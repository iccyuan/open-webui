from typing import Optional
import io
import re
import base64
import json
import asyncio
import logging

from open_webui.models.groups import Groups
from open_webui.models.models import (
    ModelForm,
    ModelMeta,
    ModelModel,
    ModelParams,
    ModelResponse,
    ModelListResponse,
    ModelAccessListResponse,
    ModelAccessResponse,
    Models,
)
from open_webui.models.access_grants import AccessGrants

from pydantic import BaseModel
from open_webui.constants import ERROR_MESSAGES
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    Response,
)
from fastapi.responses import FileResponse, StreamingResponse


from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.utils.access_control import has_permission, filter_allowed_access_grants
from open_webui.config import BYPASS_ADMIN_ACCESS_CONTROL, STATIC_DIR
from open_webui.internal.db import get_session
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

router = APIRouter()


def is_valid_model_id(model_id: str) -> bool:
    return model_id and len(model_id) <= 256


###########################
# GetModels
###########################


PAGE_ITEM_COUNT = 30


@router.get(
    "/list", response_model=ModelAccessListResponse
)  # do NOT use "/" as path, conflicts with main.py
async def get_models(
    query: Optional[str] = None,
    view_option: Optional[str] = None,
    tag: Optional[str] = None,
    order_by: Optional[str] = None,
    direction: Optional[str] = None,
    page: Optional[int] = 1,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):

    limit = PAGE_ITEM_COUNT

    page = max(1, page)
    skip = (page - 1) * limit

    filter = {}
    if query:
        filter["query"] = query
    if view_option:
        filter["view_option"] = view_option
    if tag:
        filter["tag"] = tag
    if order_by:
        filter["order_by"] = order_by
    if direction:
        filter["direction"] = direction

    # Pre-fetch user group IDs once - used for both filter and write_access check
    groups = Groups.get_groups_by_member_id(user.id, db=db)
    user_group_ids = {group.id for group in groups}

    if not user.role == "admin" or not BYPASS_ADMIN_ACCESS_CONTROL:
        if groups:
            filter["group_ids"] = [group.id for group in groups]

        filter["user_id"] = user.id

    result = Models.search_models(user.id, filter=filter, skip=skip, limit=limit, db=db)

    # Batch-fetch writable model IDs in a single query instead of N has_access calls
    model_ids = [model.id for model in result.items]
    writable_model_ids = AccessGrants.get_accessible_resource_ids(
        user_id=user.id,
        resource_type="model",
        resource_ids=model_ids,
        permission="write",
        user_group_ids=user_group_ids,
        db=db,
    )

    return ModelAccessListResponse(
        items=[
            ModelAccessResponse(
                **model.model_dump(),
                write_access=(
                    (user.role == "admin" and BYPASS_ADMIN_ACCESS_CONTROL)
                    or user.id == model.user_id
                    or model.id in writable_model_ids
                ),
            )
            for model in result.items
        ],
        total=result.total,
    )


###########################
# GetBaseModels
###########################


@router.get("/base", response_model=list[ModelResponse])
async def get_base_models(
    user=Depends(get_admin_user), db: Session = Depends(get_session)
):
    return Models.get_base_models(db=db)


###########################
# GetModelTags
###########################


@router.get("/tags", response_model=list[str])
async def get_model_tags(
    user=Depends(get_verified_user), db: Session = Depends(get_session)
):
    if user.role == "admin" and BYPASS_ADMIN_ACCESS_CONTROL:
        models = Models.get_models(db=db)
    else:
        models = Models.get_models_by_user_id(user.id, db=db)

    tags_set = set()
    for model in models:
        if model.meta:
            meta = model.meta.model_dump()
            for tag in meta.get("tags", []):
                tags_set.add((tag.get("name")))

    tags = [tag for tag in tags_set]
    tags.sort()
    return tags


############################
# CreateNewModel
############################


@router.post("/create", response_model=Optional[ModelModel])
async def create_new_model(
    request: Request,
    form_data: ModelForm,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    if user.role != "admin" and not has_permission(
        user.id, "workspace.models", request.app.state.config.USER_PERMISSIONS, db=db
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    model = Models.get_model_by_id(form_data.id, db=db)
    if model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.MODEL_ID_TAKEN,
        )

    if not is_valid_model_id(form_data.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.MODEL_ID_TOO_LONG,
        )

    else:
        model = Models.insert_new_model(form_data, user.id, db=db)
        if model:
            return model
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.DEFAULT(),
            )


############################
# ExportModels
############################


@router.get("/export", response_model=list[ModelModel])
async def export_models(
    request: Request,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    if user.role != "admin" and not has_permission(
        user.id,
        "workspace.models_export",
        request.app.state.config.USER_PERMISSIONS,
        db=db,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    if user.role == "admin" and BYPASS_ADMIN_ACCESS_CONTROL:
        return Models.get_models(db=db)
    else:
        return Models.get_models_by_user_id(user.id, db=db)


############################
# ImportModels
############################


class ModelsImportForm(BaseModel):
    models: list[dict]


@router.post("/import", response_model=bool)
async def import_models(
    request: Request,
    user=Depends(get_verified_user),
    form_data: ModelsImportForm = (...),
    db: Session = Depends(get_session),
):
    if user.role != "admin" and not has_permission(
        user.id,
        "workspace.models_import",
        request.app.state.config.USER_PERMISSIONS,
        db=db,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )
    try:
        data = form_data.models
        if isinstance(data, list):
            # Batch-fetch all existing models in one query to avoid N+1
            model_ids = [
                model_data.get("id")
                for model_data in data
                if model_data.get("id") and is_valid_model_id(model_data.get("id"))
            ]
            existing_models = {
                model.id: model
                for model in (
                    Models.get_models_by_ids(model_ids, db=db) if model_ids else []
                )
            }

            for model_data in data:
                # Here, you can add logic to validate model_data if needed
                model_id = model_data.get("id")

                if model_id and is_valid_model_id(model_id):
                    existing_model = existing_models.get(model_id)
                    if existing_model:
                        # Update existing model
                        model_data["meta"] = model_data.get("meta", {})
                        model_data["params"] = model_data.get("params", {})

                        updated_model = ModelForm(
                            **{**existing_model.model_dump(), **model_data}
                        )
                        Models.update_model_by_id(model_id, updated_model, db=db)
                    else:
                        # Insert new model
                        model_data["meta"] = model_data.get("meta", {})
                        model_data["params"] = model_data.get("params", {})
                        new_model = ModelForm(**model_data)
                        Models.insert_new_model(
                            user_id=user.id, form_data=new_model, db=db
                        )
            return True
        else:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


############################
# SyncModels
############################


class SyncModelsForm(BaseModel):
    models: list[ModelModel] = []


@router.post("/sync", response_model=list[ModelModel])
async def sync_models(
    request: Request,
    form_data: SyncModelsForm,
    user=Depends(get_admin_user),
    db: Session = Depends(get_session),
):
    return Models.sync_models(user.id, form_data.models, db=db)


###########################
# GetModelById
###########################


class ModelIdForm(BaseModel):
    id: str


# Note: We're not using the typical url path param here, but instead using a query parameter to allow '/' in the id
@router.get("/model", response_model=Optional[ModelAccessResponse])
async def get_model_by_id(
    id: str, user=Depends(get_verified_user), db: Session = Depends(get_session)
):
    model = Models.get_model_by_id(id, db=db)
    if model:
        if (
            (user.role == "admin" and BYPASS_ADMIN_ACCESS_CONTROL)
            or model.user_id == user.id
            or AccessGrants.has_access(
                user_id=user.id,
                resource_type="model",
                resource_id=model.id,
                permission="read",
                db=db,
            )
        ):
            return ModelAccessResponse(
                **model.model_dump(),
                write_access=(
                    (user.role == "admin" and BYPASS_ADMIN_ACCESS_CONTROL)
                    or user.id == model.user_id
                    or AccessGrants.has_access(
                        user_id=user.id,
                        resource_type="model",
                        resource_id=model.id,
                        permission="write",
                        db=db,
                    )
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


###########################
# Model Profile Image Utils
###########################

# Inline SVG icons for well-known AI providers.
# Each SVG uses the provider's official brand colors so they look great
# on both light and dark backgrounds without any external network dependency.
PROVIDER_SVGS: dict[str, str] = {
    "openai": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#000"/>
<g transform="translate(20, 20) scale(1.46)">
<path d="M37.532 16.87a9.963 9.963 0 0 0-.856-8.184 10.078 10.078 0 0 0-10.855-4.835A9.964 9.964 0 0 0 18.306.5a10.079 10.079 0 0 0-9.614 6.977 9.967 9.967 0 0 0-6.664 4.834 10.08 10.08 0 0 0 1.24 11.817 9.965 9.965 0 0 0 .856 8.185 10.079 10.079 0 0 0 10.855 4.835 9.965 9.965 0 0 0 7.516 3.35 10.078 10.078 0 0 0 9.617-6.981 9.967 9.967 0 0 0 6.663-4.834 10.079 10.079 0 0 0-1.243-11.813zM22.498 37.886a7.474 7.474 0 0 1-4.799-1.735c.061-.033.168-.091.237-.134l7.964-4.6a1.294 1.294 0 0 0 .655-1.134V19.054l3.366 1.944a.12.12 0 0 1 .066.092v9.299a7.505 7.505 0 0 1-7.49 7.496zM6.392 31.006a7.471 7.471 0 0 1-.894-5.023c.06.036.162.099.237.141l7.964 4.6a1.297 1.297 0 0 0 1.308 0l9.724-5.614v3.888a.12.12 0 0 1-.048.103L16.5 33.798a7.505 7.505 0 0 1-10.108-2.792zm-2.32-17.126a7.47 7.47 0 0 1 3.91-3.293v9.206a1.294 1.294 0 0 0 .654 1.132l9.723 5.614-3.366 1.944a.12.12 0 0 1-.114.012L7.044 23.86a7.504 7.504 0 0 1-2.972-10.18zm27.658 6.437l-9.724-5.615 3.367-1.943a.121.121 0 0 1 .114-.012l7.857 4.533a7.504 7.504 0 0 1-1.158 13.528v-9.207a1.294 1.294 0 0 0-.456-1.284zm3.35-5.043c-.059-.037-.162-.099-.236-.141l-7.965-4.6a1.298 1.298 0 0 0-1.308 0l-9.723 5.614v-3.888a.12.12 0 0 1 .048-.103l7.883-4.551a7.504 7.504 0 0 1 11.3 7.669zm-21.063 6.929l-3.367-1.944a.12.12 0 0 1-.065-.092v-9.299a7.504 7.504 0 0 1 12.301-5.762 6.94 6.94 0 0 0-.236.134l-7.965 4.6a1.294 1.294 0 0 0-.654 1.132l-.014 11.231zm1.829-3.943l4.33-2.501 4.332 2.5v4.999l-4.331 2.5-4.331-2.5V19.16z" fill="white"/>
</g>
</svg>""",

    "claude": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1.2 -1.2 26.4 26.4"><rect x="-1.2" y="-1.2" width="26.4" height="26.4" rx="13.2" fill="#D97757" /><path fill="white" d="m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z"/></svg>""",

    "anthropic": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#D97757"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M13.827 5.47h2.405L21 18.53h-2.354l-1.11-2.933h-5.12l-1.11 2.933H9L13.827 5.47zm2.07 8.241-1.868-4.935-1.868 4.935h3.736zM7.44 5.47H5v13.06h2.44V5.47z" fill="white"/>
</g>
</svg>""",

    "google": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="white"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
</g>
</svg>""",

    "gemini": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1.2 -1.2 26.4 26.4"><rect x="-1.2" y="-1.2" width="26.4" height="26.4" rx="13.2" fill="#1A73E8"/><path d="M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81" fill="white"/></svg>""",

    "meta": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#0866FF"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10c2.65 0 5.06-1.03 6.84-2.71a9.96 9.96 0 0 0 6.84 2.71c5.52 0 10-4.48 10-10S31.19 2 25.67 2a9.96 9.96 0 0 0-6.83 2.7A9.95 9.95 0 0 0 12 2zm0 4.14A5.85 5.85 0 0 1 17.85 12 5.85 5.85 0 0 1 12 17.85a5.85 5.85 0 0 1-4.14-1.72A5.85 5.85 0 0 1 6.15 12a5.85 5.85 0 0 1 1.71-4.14A5.85 5.85 0 0 1 12 6.14zm13.67 0c2.25 0 4.25 1.28 5.23 3.19.06.12.1.25.13.38.29.98.49 2.03.49 3.14 0 3.23-2.61 5.85-5.85 5.85s-5.85-2.62-5.85-5.85c0-1.12.21-2.18.51-3.16.03-.11.06-.21.1-.31a5.84 5.84 0 0 1 5.24-3.24Z" fill="white"/>
</g>
</svg>""",

    "mistral": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#FF7000"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M4 4h4v4H4V4zm6 6h4v4h-4v-4zm0 6h4v4h-4v-4zm6-6h4v4h-4v-4zm-6-6h4v4h-4v-4zm-6 6h4v4H4v-4zm12 6h4v4h-4v-4zm0-12h4v4h-4V4zM4 16h4v4H4v-4z" fill="white"/>
</g>
</svg>""",

    "deepseek": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#4D6BFE"/>
<text x="50" y="66" font-family="system-ui, -apple-system, sans-serif" font-size="44" font-weight="800" text-anchor="middle" fill="white" letter-spacing="-2">DS</text>
</svg>""",

    "alibabacloud": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#6156e5"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" fill="white"/>
</g>
</svg>""",

    "microsoft": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="white"/>
<g transform="translate(20, 20) scale(2.5)">
<rect x="1" y="1" width="10" height="10" fill="#f25022"/>
<rect x="13" y="1" width="10" height="10" fill="#7fba00"/>
<rect x="1" y="13" width="10" height="10" fill="#00a4ef"/>
<rect x="13" y="13" width="10" height="10" fill="#ffb900"/>
</g>
</svg>""",

    "copilot": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1.2 -1.2 26.4 26.4">
<circle cx="12" cy="12" r="13.2" fill="#000000"/>
<path d="M23.922 16.997C23.061 18.492 18.063 22.02 12 22.02 5.937 22.02.939 18.492.078 16.997A.641.641 0 0 1 0 16.741v-2.869a.883.883 0 0 1 .053-.22c.372-.935 1.347-2.292 2.605-2.656.167-.429.414-1.055.644-1.517a10.098 10.098 0 0 1-.052-1.086c0-1.331.282-2.499 1.132-3.368.397-.406.89-.717 1.474-.952C7.255 2.937 9.248 1.98 11.978 1.98c2.731 0 4.767.957 6.166 2.093.584.235 1.077.546 1.474.952.85.869 1.132 2.037 1.132 3.368 0 .368-.014.733-.052 1.086.23.462.477 1.088.644 1.517 1.258.364 2.233 1.721 2.605 2.656a.841.841 0 0 1 .053.22v2.869a.641.641 0 0 1-.078.256Zm-11.75-5.992h-.344a4.359 4.359 0 0 1-.355.508c-.77.947-1.918 1.492-3.508 1.492-1.725 0-2.989-.359-3.782-1.259a2.137 2.137 0 0 1-.085-.104L4 11.746v6.585c1.435.779 4.514 2.179 8 2.179 3.486 0 6.565-1.4 8-2.179v-6.585l-.098-.104s-.033.045-.085.104c-.793.9-2.057 1.259-3.782 1.259-1.59 0-2.738-.545-3.508-1.492a4.359 4.359 0 0 1-.355-.508Zm2.328 3.25c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm-5 0c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm3.313-6.185c.136 1.057.403 1.913.878 2.497.442.544 1.134.938 2.344.938 1.573 0 2.292-.337 2.657-.751.384-.435.558-1.15.558-2.361 0-1.14-.243-1.847-.705-2.319-.477-.488-1.319-.862-2.824-1.025-1.487-.161-2.192.138-2.533.529-.269.307-.437.808-.438 1.578v.021c0 .265.021.562.063.893Zm-1.626 0c.042-.331.063-.628.063-.894v-.02c-.001-.77-.169-1.271-.438-1.578-.341-.391-1.046-.69-2.533-.529-1.505.163-2.347.537-2.824 1.025-.462.472-.705 1.179-.705 2.319 0 1.211.175 1.926.558 2.361.365.414 1.084.751 2.657.751 1.21 0 1.902-.394 2.344-.938.475-.584.742-1.44.878-2.497Z" fill="white"/>
</svg>""",

    "perplexity": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#1C1C1C"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M12 22a.96.96 0 0 1-.96-.96v-7.38H5.98V7.5a.96.96 0 0 1 .96-.96h10.12a.96.96 0 0 1 .96.96v6.16h-5.06v7.38a.96.96 0 0 1-.96.96h0Z" fill="white"/>
</g>
</svg>""",

    "x": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#000"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z" fill="white"/>
</g>
</svg>""",

    "ollama": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#F0F0F0"/>
<g transform="translate(15, 14) scale(2.1)">
<ellipse cx="16.5" cy="11.5" rx="7.5" ry="7.5" fill="none" stroke="#222" stroke-width="2"/>
<circle cx="13.5" cy="10" r="1.5" fill="#222"/>
<circle cx="19.5" cy="10" r="1.5" fill="#222"/>
<ellipse cx="16.5" cy="22.5" rx="6.5" ry="7" fill="none" stroke="#222" stroke-width="2"/>
<line x1="12" y1="18.5" x2="10" y2="15.5" stroke="#222" stroke-width="2" stroke-linecap="round"/>
<line x1="21" y1="18.5" x2="23" y2="15.5" stroke="#222" stroke-width="2" stroke-linecap="round"/>
</g>
</svg>""",

    "cohere": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 110 110">
<circle cx="50" cy="50" r="50" fill="#FAF5F1"/>
<g transform="translate(18, 18) scale(2.66)">
<circle cx="12" cy="12" r="12" fill="#39594D"/>
<circle cx="9" cy="12" r="3.75" fill="#1333F2"/>
<circle cx="15.75" cy="9" r="2.25" fill="#FF7759"/>
<circle cx="15.75" cy="15.75" r="1.5" fill="#FFCA74"/>
</g>
</svg>""",
}


def get_provider_from_model_id(model_id: str) -> str | None:
    """Detect the AI provider from a model ID string."""
    model_id_lower = model_id.lower()
    
    # Support 3rd party model formats like openrouter/openai/gpt-4o or litellm/anthropic/claude-3
    if "/" in model_id_lower:
        base_name = model_id_lower.split("/")[-1]
    else:
        base_name = model_id_lower

    # OpenAI: verify base_name for gpt-, o1, etc.
    OPENAI_PREFIXES = [
        "gpt-", "dall-e", "text-embedding", "whisper", "babbage", "davinci", "chatgpt", "o1", "o3", "o4"
    ]
    if any(base_name.startswith(p) for p in OPENAI_PREFIXES) or "openai" in model_id_lower:
        return "openai"

    PROVIDER_PATTERNS = [
        (["claude"], "claude"),
        (["anthropic"], "anthropic"),
        (["gemini"], "gemini"),
        (["gemma", "palm", "google"], "google"),
        (["llama", "meta-llama", "meta/llama", "meta"], "meta"),
        (["mistral", "mixtral", "codestral", "devstral", "mathstral"], "mistral"),
        (["command-r", "cohere"], "cohere"),
        (["deepseek"], "deepseek"),
        (["qwen", "qwq", "qvq", "alibabacloud"], "alibabacloud"),
        (["copilot"], "copilot"),
        (["phi-", "phi/", "microsoft"], "microsoft"),
        (["sonar", "pplx", "perplexity"], "perplexity"),
        (["grok", "xai"], "x"),
        (["ollama"], "ollama"),
    ]

    for keywords, provider in PROVIDER_PATTERNS:
        if any(kw in model_id_lower for kw in keywords):
            return provider

    return None


@router.get("/model/profile/image")
def get_model_profile_image(id: str, user=Depends(get_verified_user)):
    model = Models.get_model_by_id(id)
    provider = get_provider_from_model_id(id)

    if model:
        etag = f'"{model.updated_at}"' if model.updated_at else None

        if model.meta.profile_image_url:
            # If it's a data image (user uploaded custom image), we always respect it.
            if model.meta.profile_image_url.startswith("data:image"):
                try:
                    header, base64_data = model.meta.profile_image_url.split(",", 1)
                    image_data = base64.b64decode(base64_data)
                    image_buffer = io.BytesIO(image_data)
                    media_type = header.split(";")[0].lstrip("data:")

                    headers = {"Content-Disposition": "inline"}
                    if etag:
                        headers["ETag"] = etag

                    return StreamingResponse(
                        image_buffer,
                        media_type=media_type,
                        headers=headers,
                    )
                except Exception as e:
                    pass
            # If it's an external URL, only use it if we DON'T have a beautiful local official SVG for it.
            elif model.meta.profile_image_url.startswith("http"):
                if not provider or provider not in PROVIDER_SVGS:
                    return Response(
                        status_code=status.HTTP_302_FOUND,
                        headers={"Location": model.meta.profile_image_url},
                    )

    # Use the local provider's official SVG icon inline
    if provider and provider in PROVIDER_SVGS:
        return Response(
            content=PROVIDER_SVGS[provider],
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=86400"},
        )

    return FileResponse(f"{STATIC_DIR}/favicon.png")




############################
# ToggleModelById
############################


@router.post("/model/toggle", response_model=Optional[ModelResponse])
async def toggle_model_by_id(
    id: str, user=Depends(get_verified_user), db: Session = Depends(get_session)
):
    model = Models.get_model_by_id(id, db=db)
    if model:
        if (
            user.role == "admin"
            or model.user_id == user.id
            or AccessGrants.has_access(
                user_id=user.id,
                resource_type="model",
                resource_id=model.id,
                permission="write",
                db=db,
            )
        ):
            model = Models.toggle_model_by_id(id, db=db)

            if model:
                return model
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ERROR_MESSAGES.DEFAULT("Error updating function"),
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.UNAUTHORIZED,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateModelById
############################


@router.post("/model/update", response_model=Optional[ModelModel])
async def update_model_by_id(
    form_data: ModelForm,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    model = Models.get_model_by_id(form_data.id, db=db)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    if (
        model.user_id != user.id
        and not AccessGrants.has_access(
            user_id=user.id,
            resource_type="model",
            resource_id=model.id,
            permission="write",
            db=db,
        )
        and user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )

    model = Models.update_model_by_id(
        form_data.id, ModelForm(**form_data.model_dump()), db=db
    )
    return model


############################
# UpdateModelAccessById
############################


class ModelAccessGrantsForm(BaseModel):
    id: str
    name: Optional[str] = None
    access_grants: list[dict]


@router.post("/model/access/update", response_model=Optional[ModelModel])
async def update_model_access_by_id(
    request: Request,
    form_data: ModelAccessGrantsForm,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    model = Models.get_model_by_id(form_data.id, db=db)

    # Non-preset models (e.g. direct Ollama/OpenAI models) may not have a DB
    # entry yet. Create a minimal one so access grants can be stored.
    if not model:
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
            )
        model = Models.insert_new_model(
            ModelForm(
                id=form_data.id,
                name=form_data.name or form_data.id,
                meta=ModelMeta(),
                params=ModelParams(),
            ),
            user.id,
            db=db,
        )
        if not model:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ERROR_MESSAGES.DEFAULT("Error creating model entry"),
            )

    if (
        model.user_id != user.id
        and not AccessGrants.has_access(
            user_id=user.id,
            resource_type="model",
            resource_id=model.id,
            permission="write",
            db=db,
        )
        and user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )

    form_data.access_grants = filter_allowed_access_grants(
        request.app.state.config.USER_PERMISSIONS,
        user.id,
        user.role,
        form_data.access_grants,
        "sharing.public_models",
    )

    AccessGrants.set_access_grants(
        "model", form_data.id, form_data.access_grants, db=db
    )

    return Models.get_model_by_id(form_data.id, db=db)


############################
# DeleteModelById
############################


@router.post("/model/delete", response_model=bool)
async def delete_model_by_id(
    form_data: ModelIdForm,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    model = Models.get_model_by_id(form_data.id, db=db)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    if (
        user.role != "admin"
        and model.user_id != user.id
        and not AccessGrants.has_access(
            user_id=user.id,
            resource_type="model",
            resource_id=model.id,
            permission="write",
            db=db,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    result = Models.delete_model_by_id(form_data.id, db=db)
    return result


@router.delete("/delete/all", response_model=bool)
async def delete_all_models(
    user=Depends(get_admin_user), db: Session = Depends(get_session)
):
    result = Models.delete_all_models(db=db)
    return result

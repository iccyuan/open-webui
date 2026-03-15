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
    "openai": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#000"/>
<g transform="translate(20, 20) scale(1.46)">
<path d="M37.532 16.87a9.963 9.963 0 0 0-.856-8.184 10.078 10.078 0 0 0-10.855-4.835A9.964 9.964 0 0 0 18.306.5a10.079 10.079 0 0 0-9.614 6.977 9.967 9.967 0 0 0-6.664 4.834 10.08 10.08 0 0 0 1.24 11.817 9.965 9.965 0 0 0 .856 8.185 10.079 10.079 0 0 0 10.855 4.835 9.965 9.965 0 0 0 7.516 3.35 10.078 10.078 0 0 0 9.617-6.981 9.967 9.967 0 0 0 6.663-4.834 10.079 10.079 0 0 0-1.243-11.813zM22.498 37.886a7.474 7.474 0 0 1-4.799-1.735c.061-.033.168-.091.237-.134l7.964-4.6a1.294 1.294 0 0 0 .655-1.134V19.054l3.366 1.944a.12.12 0 0 1 .066.092v9.299a7.505 7.505 0 0 1-7.49 7.496zM6.392 31.006a7.471 7.471 0 0 1-.894-5.023c.06.036.162.099.237.141l7.964 4.6a1.297 1.297 0 0 0 1.308 0l9.724-5.614v3.888a.12.12 0 0 1-.048.103L16.5 33.798a7.505 7.505 0 0 1-10.108-2.792zm-2.32-17.126a7.47 7.47 0 0 1 3.91-3.293v9.206a1.294 1.294 0 0 0 .654 1.132l9.723 5.614-3.366 1.944a.12.12 0 0 1-.114.012L7.044 23.86a7.504 7.504 0 0 1-2.972-10.18zm27.658 6.437l-9.724-5.615 3.367-1.943a.121.121 0 0 1 .114-.012l7.857 4.533a7.504 7.504 0 0 1-1.158 13.528v-9.207a1.294 1.294 0 0 0-.456-1.284zm3.35-5.043c-.059-.037-.162-.099-.236-.141l-7.965-4.6a1.298 1.298 0 0 0-1.308 0l-9.723 5.614v-3.888a.12.12 0 0 1 .048-.103l7.883-4.551a7.504 7.504 0 0 1 11.3 7.669zm-21.063 6.929l-3.367-1.944a.12.12 0 0 1-.065-.092v-9.299a7.504 7.504 0 0 1 12.301-5.762 6.94 6.94 0 0 0-.236.134l-7.965 4.6a1.294 1.294 0 0 0-.654 1.132l-.014 11.231zm1.829-3.943l4.33-2.501 4.332 2.5v4.999l-4.331 2.5-4.331-2.5V19.16z" fill="white"/>
</g>
</svg>""",

    "anthropic": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#D97757"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M13.827 5.47h2.405L21 18.53h-2.354l-1.11-2.933h-5.12l-1.11 2.933H9L13.827 5.47zm2.07 8.241-1.868-4.935-1.868 4.935h3.736zM7.44 5.47H5v13.06h2.44V5.47z" fill="white"/>
</g>
</svg>""",

    "google": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="white"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
</g>
</svg>""",

    "meta": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#0866FF"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10c2.65 0 5.06-1.03 6.84-2.71a9.96 9.96 0 0 0 6.84 2.71c5.52 0 10-4.48 10-10S31.19 2 25.67 2a9.96 9.96 0 0 0-6.83 2.7A9.95 9.95 0 0 0 12 2zm0 4.14A5.85 5.85 0 0 1 17.85 12 5.85 5.85 0 0 1 12 17.85a5.85 5.85 0 0 1-4.14-1.72A5.85 5.85 0 0 1 6.15 12a5.85 5.85 0 0 1 1.71-4.14A5.85 5.85 0 0 1 12 6.14zm13.67 0c2.25 0 4.25 1.28 5.23 3.19.06.12.1.25.13.38.29.98.49 2.03.49 3.14 0 3.23-2.61 5.85-5.85 5.85s-5.85-2.62-5.85-5.85c0-1.12.21-2.18.51-3.16.03-.11.06-.21.1-.31a5.84 5.84 0 0 1 5.24-3.24Z" fill="white"/>
</g>
</svg>""",

    "mistral": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#FF7000"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M4 4h4v4H4V4zm6 6h4v4h-4v-4zm0 6h4v4h-4v-4zm6-6h4v4h-4v-4zm-6-6h4v4h-4v-4zm-6 6h4v4H4v-4zm12 6h4v4h-4v-4zm0-12h4v4h-4V4zM4 16h4v4H4v-4z" fill="white"/>
</g>
</svg>""",

    "deepseek": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#4D6BFE"/>
<text x="50" y="66" font-family="system-ui, -apple-system, sans-serif" font-size="44" font-weight="800" text-anchor="middle" fill="white" letter-spacing="-2">DS</text>
</svg>""",

    "alibabacloud": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#6156e5"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" fill="white"/>
</g>
</svg>""",

    "microsoft": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="white"/>
<g transform="translate(20, 20) scale(2.5)">
<rect x="1" y="1" width="10" height="10" fill="#f25022"/>
<rect x="13" y="1" width="10" height="10" fill="#7fba00"/>
<rect x="1" y="13" width="10" height="10" fill="#00a4ef"/>
<rect x="13" y="13" width="10" height="10" fill="#ffb900"/>
</g>
</svg>""",

    "perplexity": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#1C1C1C"/>
<g transform="translate(18, 18) scale(2.66)">
<path d="M12 22a.96.96 0 0 1-.96-.96v-7.38H5.98V7.5a.96.96 0 0 1 .96-.96h10.12a.96.96 0 0 1 .96.96v6.16h-5.06v7.38a.96.96 0 0 1-.96.96h0Z" fill="white"/>
</g>
</svg>""",

    "x": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="50" fill="#000"/>
<g transform="translate(20, 20) scale(2.5)">
<path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z" fill="white"/>
</g>
</svg>""",

    "ollama": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
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

    "cohere": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
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

    # OpenAI: prefix-based matching
    OPENAI_PREFIXES = [
        "gpt-", "dall-e", "text-embedding-ada", "whisper", "babbage", "davinci",
    ]
    # Also match short standalone OpenAI model names: o1, o3, o4, o1-mini, o3-mini, etc.
    OPENAI_SHORT = re.compile(r"^o[134](-|$)")
    if any(model_id_lower.startswith(p) for p in OPENAI_PREFIXES) or OPENAI_SHORT.match(model_id_lower):
        return "openai"

    PROVIDER_PATTERNS = [
        (["claude"], "anthropic"),
        (["gemini", "gemma", "palm"], "google"),
        (["llama", "meta-llama", "meta/llama"], "meta"),
        (["mistral", "mixtral", "codestral", "devstral", "mathstral"], "mistral"),
        (["command-r", "cohere/"], "cohere"),
        (["deepseek"], "deepseek"),
        (["qwen", "qwq", "qvq"], "alibabacloud"),
        (["phi-", "phi/", "copilot", "microsoft/"], "microsoft"),
        (["sonar", "pplx-", "perplexity"], "perplexity"),
        (["grok", "xai/"], "x"),
        (["ollama"], "ollama"),
    ]

    for keywords, provider in PROVIDER_PATTERNS:
        if any(kw in model_id_lower for kw in keywords):
            return provider

    return None


@router.get("/model/profile/image")
def get_model_profile_image(id: str, user=Depends(get_verified_user)):
    model = Models.get_model_by_id(id)

    if model:
        etag = f'"{model.updated_at}"' if model.updated_at else None

        if model.meta.profile_image_url:
            if model.meta.profile_image_url.startswith("http"):
                return Response(
                    status_code=status.HTTP_302_FOUND,
                    headers={"Location": model.meta.profile_image_url},
                )
            elif model.meta.profile_image_url.startswith("data:image"):
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

    # No custom image: serve the provider's official SVG icon inline
    provider = get_provider_from_model_id(id)
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

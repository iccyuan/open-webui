<script lang="ts">
	import { toast } from 'svelte-sonner';

	import { tick, getContext, onMount, createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	import { settings } from '$lib/stores';
	import { copyToClipboard } from '$lib/utils';

	import LazyLoad from '$lib/components/common/LazyLoad.svelte';
	import MultiResponseMessages from './MultiResponseMessages.svelte';
	import ResponseMessage from './ResponseMessage.svelte';
	import UserMessage from './UserMessage.svelte';

	export let chatId;
	export let selectedModels = [];
	export let idx = 0;

	export let history;
	export let messageId;

	export let user;

	export let setInputText: Function = () => {};
	export let gotoMessage;
	export let showPreviousMessage;
	export let showNextMessage;
	export let updateChat;

	export let editMessage;
	export let saveMessage;
	export let deleteMessage;
	export let rateMessage;
	export let actionMessage;
	export let submitMessage;

	export let regenerateResponse;
	export let continueResponse;
	export let mergeResponses;

	export let addMessages;
	export let triggerScroll;
	export let readOnly = false;
	export let editCodeBlock = true;
	export let topPadding = false;
	export let isLastMessage = false;
	export let forceInitialRender = false;
</script>

<div
	role="listitem"
	id="message-{messageId}"
	data-role={history.messages[messageId]?.role}
	class="flex flex-col justify-between px-5 mb-1.5 w-full {($settings?.widescreenMode ?? null)
		? 'max-w-full'
		: 'max-w-5xl'} mx-auto rounded-lg group"
>
	{#if history.messages[messageId]}
		<LazyLoad className="w-full" rootMargin="500px" keepAlive={isLastMessage} {forceInitialRender}>
			{#if history.messages[messageId].role === 'user'}
				<UserMessage
					{user}
					{chatId}
					{history}
					{messageId}
					isFirstMessage={idx === 0}
					siblings={history.messages[messageId].parentId !== null
						? (history.messages[history.messages[messageId].parentId]?.childrenIds ?? [])
						: (Object.values(history.messages)
								.filter((message) => message.parentId === null)
								.map((message) => message.id) ?? [])}
					{gotoMessage}
					{showPreviousMessage}
					{showNextMessage}
					{editMessage}
					{deleteMessage}
					{readOnly}
					{editCodeBlock}
					{topPadding}
				/>
			{:else if (history.messages[history.messages[messageId].parentId]?.models?.length ?? 1) === 1}
				<ResponseMessage
					{chatId}
					{history}
					{messageId}
					{selectedModels}
					isLastMessage={messageId === history.currentId}
					siblings={history.messages[history.messages[messageId].parentId]?.childrenIds ?? []}
					{setInputText}
					{gotoMessage}
					{showPreviousMessage}
					{showNextMessage}
					{updateChat}
					{editMessage}
					{saveMessage}
					{rateMessage}
					{actionMessage}
					{submitMessage}
					{deleteMessage}
					{continueResponse}
					{regenerateResponse}
					{addMessages}
					{readOnly}
					{editCodeBlock}
					{topPadding}
				/>
			{:else}
				{#key messageId}
					<MultiResponseMessages
						bind:history
						{chatId}
						{messageId}
						{selectedModels}
						isLastMessage={messageId === history?.currentId}
						{setInputText}
						{updateChat}
						{editMessage}
						{saveMessage}
						{rateMessage}
						{actionMessage}
						{submitMessage}
						{deleteMessage}
						{continueResponse}
						{regenerateResponse}
						{mergeResponses}
						{triggerScroll}
						{addMessages}
						{readOnly}
						{editCodeBlock}
						{topPadding}
					/>
				{/key}
			{/if}
			<svelte:fragment slot="placeholder">
				<div style="min-height: 3rem;" />
			</svelte:fragment>
		</LazyLoad>
	{/if}
</div>

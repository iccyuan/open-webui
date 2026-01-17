<script lang="ts">
	import { copyToClipboard, unescapeHtml } from '$lib/utils';
	import { toast } from 'svelte-sonner';
	import { fly } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	import { getContext } from 'svelte';

	const i18n = getContext('i18n');

	export let token;
	export let done = true;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
{#if done}
	<code
		class="codespan cursor-pointer"
		on:click={() => {
			copyToClipboard(unescapeHtml(token.text));
			toast.success($i18n.t('Copied to clipboard'));
		}}>{unescapeHtml(token.text)}</code
	>
{:else}
	<code
		in:fly={{ x: -6, duration: 180, easing: cubicOut }}
		class="codespan cursor-pointer streaming-code"
		on:click={() => {
			copyToClipboard(unescapeHtml(token.text));
			toast.success($i18n.t('Copied to clipboard'));
		}}>{unescapeHtml(token.text)}</code
	>
{/if}

<style>
	.streaming-code {
		display: inline-block;
		will-change: transform, opacity;
		animation: smooth-code-appear 0.18s cubic-bezier(0.33, 1, 0.68, 1) forwards;
	}

	@keyframes smooth-code-appear {
		from {
			opacity: 0;
			transform: translateX(-6px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}
</style>

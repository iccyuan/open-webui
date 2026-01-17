<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import { cubicOut, cubicInOut } from 'svelte/easing';

	export let token;
	export let done = true;
	export let streamMode = 'word';

	let rawText = '';
	let words = [];
	let lines = [];
	$: rawText = token?.raw ?? '';
	$: words = rawText.split(' ');
	$: lines = rawText.split('\n');
</script>

{#if done}
	{token?.raw}
{:else if streamMode === 'line'}
	{#each lines as line, lineIdx}
		<span class="streaming-line" in:fly={{ y: -8, duration: 200, easing: cubicOut }}>
			{line}
		</span>
		{#if lineIdx < lines.length - 1}
			<br />
		{/if}
	{/each}
{:else}
	{#each words as text}
		<span class="streaming-word" in:fly={{ x: -6, duration: 180, easing: cubicOut }}>
			{text}{' '}
		</span>
	{/each}
{/if}

<style>
	.streaming-word,
	.streaming-line {
		display: inline-block;
		will-change: transform, opacity;
	}

	.streaming-word {
		animation: smooth-appear 0.18s cubic-bezier(0.33, 1, 0.68, 1) forwards;
	}

	.streaming-line {
		animation: smooth-line-appear 0.2s cubic-bezier(0.33, 1, 0.68, 1) forwards;
	}

	@keyframes smooth-appear {
		from {
			opacity: 0;
			transform: translateX(-6px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes smooth-line-appear {
		from {
			opacity: 0;
			transform: translateY(-8px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>

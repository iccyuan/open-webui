<script lang="ts">
	import { fade, fly } from 'svelte/transition';

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
		<span class="streaming-line" in:fly={{ y: 4, duration: 160 }}>
			{line}
		</span>
		{#if lineIdx < lines.length - 1}
			<br />
		{/if}
	{/each}
{:else}
	{#each words as text}
		<span class="streaming-word" transition:fade={{ duration: 120 }}>
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
</style>

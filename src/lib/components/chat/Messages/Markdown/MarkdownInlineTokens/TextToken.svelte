<script lang="ts">
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
		<span class="streaming-line">
			{line}
		</span>
		{#if lineIdx < lines.length - 1}
			<br />
		{/if}
	{/each}
{:else}
	{#each words as text}
		<span class="streaming-word">
			{text}{' '}
		</span>
	{/each}
{/if}

<style>
	.streaming-word,
	.streaming-line {
		display: inline-block;
		vertical-align: baseline;
	}

	.streaming-word {
		animation: smooth-appear 0.18s cubic-bezier(0.33, 1, 0.68, 1) both;
	}

	.streaming-line {
		animation: smooth-line-appear 0.2s cubic-bezier(0.33, 1, 0.68, 1) both;
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

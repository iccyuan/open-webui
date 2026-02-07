<script>
	import { onMount } from 'svelte';

	export let className = '';
	export let threshold = 0.01;
	export let rootMargin = '500px';
	export let keepAlive = false;

	let containerElement;
	let isVisible = false;
	let placeholderHeight = 0;
	let observer;

	onMount(() => {
		observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						isVisible = true;
					} else if (!keepAlive) {
						// Record current height before unmounting content
						if (containerElement && containerElement.offsetHeight > 0) {
							placeholderHeight = containerElement.offsetHeight;
						}
						isVisible = false;
					}
				});
			},
			{ threshold, rootMargin }
		);

		if (containerElement) {
			observer.observe(containerElement);
		}

		return () => {
			observer?.disconnect();
		};
	});
</script>

<div bind:this={containerElement} class={className}>
	{#if isVisible || keepAlive}
		<slot />
	{:else if placeholderHeight > 0}
		<div style="height: {placeholderHeight}px;" />
	{:else}
		<slot name="placeholder">
			<div style="min-height: 3rem;" />
		</slot>
	{/if}
</div>

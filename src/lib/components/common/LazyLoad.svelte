<script>
	import { onMount } from 'svelte';

	export let className = '';
	export let threshold = 0.1;
	export let rootMargin = '50px';
	
	let containerElement;
	let isVisible = false;
	let hasBeenVisible = false;

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					isVisible = entry.isIntersecting;
					if (isVisible && !hasBeenVisible) {
						hasBeenVisible = true;
					}
				});
			},
			{
				threshold,
				rootMargin
			}
		);

		if (containerElement) {
			observer.observe(containerElement);
		}

		return () => {
			if (containerElement) {
				observer.unobserve(containerElement);
			}
		};
	});
</script>

<div bind:this={containerElement} class={className}>
	{#if hasBeenVisible}
		<slot />
	{:else}
		<slot name="placeholder">
			<div class="min-h-20 flex items-center justify-center text-gray-400 dark:text-gray-600">
				<!-- Placeholder while loading -->
			</div>
		</slot>
	{/if}
</div>

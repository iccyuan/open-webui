<script lang="ts">
	export let className: string = 'w-5 h-5';
	export let strokeWidth: string = '1.5';
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	fill="none"
	viewBox="0 0 24 24"
	aria-hidden="true"
	stroke-width={strokeWidth}
	stroke="currentColor"
	class={className}
>
	<path
		stroke-linecap="round"
		stroke-linejoin="round"
		d="M17 17.5 22 12 17 6.5M7 6.5 2 12 7 17.5M14.5 3.5l-5 17"
	/>
</svg>

<script>
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');

	import StatusItem from './StatusHistory/StatusItem.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';

	export let statusHistory = [];
	export let expand = false;

	let showHistory = false;

	$: if (expand) {
		showHistory = true;
	}

	let history = [];
	let status = null;

	$: if (history && history.length > 0) {
		status = history.at(-1);
	}

	$: if (JSON.stringify(statusHistory) !== JSON.stringify(history)) {
		history = statusHistory;
	}

	// Check if all statuses are done
	$: isDone = status?.done === true;
</script>

{#if history && history.length > 0}
	{#if status?.hidden !== true}
		<div class="my-1">
			<!-- Header -->
			<button
				class="flex items-center gap-1.5 w-full text-left py-0.5 group"
				aria-label={$i18n.t('Toggle status history')}
				aria-expanded={showHistory}
				on:click={() => {
					showHistory = !showHistory;
				}}
			>
				<!-- Chevron -->
				<div class="text-gray-400 dark:text-gray-500 transition-transform duration-200 {showHistory ? 'rotate-90' : ''}">
					<ChevronRight className="size-3" />
				</div>

				<!-- Lightbulb Icon -->
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-4 text-purple-700 dark:text-purple-700">
					<path d="M12 .75a8.25 8.25 0 0 0-4.135 15.39c.686.398 1.115 1.008 1.134 1.623a.75.75 0 0 0 .75.737h4.502a.75.75 0 0 0 .75-.737c.02-.615.448-1.225 1.134-1.623A8.25 8.25 0 0 0 12 .75Z"/>
					<path fill-rule="evenodd" d="M9.013 19.9a.75.75 0 0 1 .877-.597 11.319 11.319 0 0 0 4.22 0 .75.75 0 1 1 .28 1.473 12.819 12.819 0 0 1-4.78 0 .75.75 0 0 1-.597-.876ZM9.754 22.344a.75.75 0 0 1 .824-.668 13.682 13.682 0 0 0 2.844 0 .75.75 0 1 1 .156 1.492 15.156 15.156 0 0 1-3.156 0 .75.75 0 0 1-.668-.824Z" clip-rule="evenodd"/>
				</svg>

				<!-- Label -->
				<span class="text-sm font-medium text-purple-700 dark:text-purple-700">
					{#if isDone}
						{$i18n.t('Thought')}
					{:else}
						{$i18n.t('Thinking')}
					{/if}
				</span>
			</button>

			<!-- Preview (when collapsed) -->
			{#if !showHistory && status}
				<div class="ml-6 text-sm text-gray-500 dark:text-gray-400 line-clamp-1">
					{status.description || status.action || ''}...
				</div>
			{/if}

			<!-- Expanded Content -->
			{#if showHistory}
				<div class="ml-6 mt-1">
					{#each history as historyStatus, idx}
						<div class="flex items-stretch gap-2 mb-0.5">
							<div>
								<div class="pt-2.5 px-1 mb-1">
									<span class="relative flex size-1.5 rounded-full justify-center items-center">
										<span class="relative inline-flex size-1.5 rounded-full bg-gray-400 dark:bg-gray-500"></span>
									</span>
								</div>
								{#if idx !== history.length - 1}
									<div class="w-[0.5px] ml-[5px] h-[calc(100%-10px)] bg-gray-300 dark:bg-gray-600"></div>
								{/if}
							</div>
							<StatusItem status={historyStatus} done={true} />
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
{/if}

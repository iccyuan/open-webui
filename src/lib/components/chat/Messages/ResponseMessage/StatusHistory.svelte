<script>
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');

	import { slide } from 'svelte/transition';

	import StatusItem from './StatusHistory/StatusItem.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import equal from 'fast-deep-equal';

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

	$: if (!equal(statusHistory, history)) {
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
				class="flex items-center gap-1.5 text-left py-0.5 group w-full"
				aria-label={$i18n.t('Toggle status history')}
				aria-expanded={showHistory}
				on:click={() => {
					showHistory = !showHistory;
				}}
			>
				<!-- Chevron -->
				<div class="shrink-0 text-gray-400 dark:text-gray-500 transition-transform duration-200 {showHistory ? 'rotate-90' : ''}">
					<ChevronRight className="size-3" />
				</div>

				<!-- Status label (always visible) -->
				{#if status}
					<span class="text-sm text-gray-500 dark:text-gray-400 truncate">
						{status.description || status.action || ''}{showHistory ? '' : '...'}
					</span>
				{/if}
			</button>

			<!-- Expanded Content -->
			{#if showHistory}
				<div transition:slide={{ duration: 200 }} class="ml-6 mt-1">
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

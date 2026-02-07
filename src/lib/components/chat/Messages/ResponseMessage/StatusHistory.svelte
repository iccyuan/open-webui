<script>
	import StatusItem from './StatusHistory/StatusItem.svelte';

	export let statusHistory = [];

	let history = [];

	$: if (JSON.stringify(statusHistory) !== JSON.stringify(history)) {
		history = statusHistory;
	}

	$: status = history && history.length > 0 ? history.at(-1) : null;
</script>

{#if history && history.length > 0}
	{#if status?.hidden !== true}
		<div class="my-1">
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
{/if}

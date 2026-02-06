<script lang="ts">
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');

	import CodeExecutionModal from './CodeExecutionModal.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import Check from '$lib/components/icons/Check.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';

	export let codeExecutions = [];

	let selectedCodeExecution = null;
	let showCodeExecutionModal = false;
	let showExecutions = false;

	$: if (codeExecutions) {
		updateSelectedCodeExecution();
	}

	const updateSelectedCodeExecution = () => {
		if (selectedCodeExecution) {
			selectedCodeExecution = codeExecutions.find(
				(execution) => execution.id === selectedCodeExecution.id
			);
		}
	};
</script>

<CodeExecutionModal bind:show={showCodeExecutionModal} codeExecution={selectedCodeExecution} />

{#if codeExecutions.length > 0}
	<div class="my-1 border border-gray-100 dark:border-gray-800 rounded-lg p-2">
		<!-- Header -->
		<button
			class="flex items-center gap-1.5 w-full text-left group"
			on:click={() => { showExecutions = !showExecutions; }}
		>
			<!-- Chevron -->
			<div class="text-gray-400 dark:text-gray-500 transition-transform duration-200 {showExecutions ? 'rotate-90' : ''}">
				<ChevronRight className="size-3" />
			</div>

			<!-- Wrench Icon -->
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-4 text-orange-500 dark:text-orange-400">
				<path fill-rule="evenodd" d="M12 6.75a5.25 5.25 0 0 1 6.775-5.025.75.75 0 0 1 .313 1.248l-3.32 3.319c.063.475.276.934.641 1.299.365.365.824.578 1.3.64l3.318-3.319a.75.75 0 0 1 1.248.313 5.25 5.25 0 0 1-5.472 6.756c-1.018-.086-1.87.1-2.309.634L7.344 21.3A3.298 3.298 0 1 1 2.7 16.657l8.684-7.151c.533-.44.72-1.291.634-2.309A5.342 5.342 0 0 1 12 6.75ZM4.117 19.125a.75.75 0 0 1 .75-.75h.008a.75.75 0 0 1 .75.75v.008a.75.75 0 0 1-.75.75h-.008a.75.75 0 0 1-.75-.75v-.008Z" clip-rule="evenodd" />
			</svg>

			<!-- Label -->
			<span class="text-sm font-medium text-orange-600 dark:text-orange-400">
				{$i18n.t('Tool Use')}
			</span>

			<!-- Tool Count (right aligned) -->
			<span class="ml-auto text-sm text-gray-400 dark:text-gray-500">
				{codeExecutions.length} {codeExecutions.length === 1 ? 'tool' : 'tools'}
			</span>
		</button>

		<!-- Expanded Content -->
		{#if showExecutions}
			<div class="mt-2 ml-5 flex flex-col gap-1">
				{#each codeExecutions as execution (execution.id)}
					<button
						class="flex items-center gap-2 py-1 px-2 -ml-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition text-left group"
						on:click={() => {
							selectedCodeExecution = execution;
							showCodeExecutionModal = true;
						}}
					>
						<!-- Status Indicator -->
						<div 
							class="size-4 flex items-center justify-center flex-shrink-0 
							{execution?.result 
								? execution.result?.error 
									? 'text-red-500' 
									: 'text-green-500' 
								: 'text-gray-400'}"
						>
							{#if execution?.result}
								{#if execution.result?.error}
									<XMark className="size-3" strokeWidth="2.5" />
								{:else if execution.result?.output}
									<Check strokeWidth="2.5" className="size-3" />
								{:else}
									<EllipsisHorizontal className="size-3" />
								{/if}
							{:else}
								<Spinner className="size-3" />
							{/if}
						</div>

						<!-- Name -->
						<span class="text-sm text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white transition line-clamp-1 {execution?.result ? '' : 'animate-pulse'}">
							{execution.name}
						</span>
					</button>
				{/each}
			</div>
		{/if}
	</div>
{/if}

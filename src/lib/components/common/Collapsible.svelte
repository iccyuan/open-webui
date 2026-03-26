<script lang="ts">
	import { decode } from 'html-entities';
	import { v4 as uuidv4 } from 'uuid';

	import { getContext } from 'svelte';
	const i18n = getContext('i18n');

	import dayjs from '$lib/dayjs';
	import duration from 'dayjs/plugin/duration';
	import relativeTime from 'dayjs/plugin/relativeTime';

	dayjs.extend(duration);
	dayjs.extend(relativeTime);

	async function loadLocale(locales) {
		if (!locales || !Array.isArray(locales)) {
			return;
		}
		for (const locale of locales) {
			try {
				dayjs.locale(locale);
				break; // Stop after successfully loading the first available locale
			} catch (error) {
				console.error(`Could not load locale '${locale}':`, error);
			}
		}
	}

	// Assuming $i18n.languages is an array of language codes
	$: loadLocale($i18n.languages);

	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	import ChevronUp from '../icons/ChevronUp.svelte';
	import ChevronDown from '../icons/ChevronDown.svelte';
	import ChevronRight from '../icons/ChevronRight.svelte';
	import Spinner from './Spinner.svelte';

	export let open = false;

	export let className = '';
	export let buttonClassName =
		'w-fit text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition';

	export let id = '';
	export let title = null;
	export let attributes = null;

	export let chevron = false;
	export let grow = false;

	export let disabled = false;
	export let messageDone = false;
	export let hide = false;

	export let onChange: Function = () => {};

	$: onChange(open);

	const collapsibleId = uuidv4();
</script>

<div {id} class={className}>
	{#if title !== null}
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			class="{buttonClassName} {disabled ? '' : 'cursor-pointer'}"
			on:pointerup={() => {
				if (!disabled) {
					open = !open;
				}
			}}
		>
			<div
				class=" w-full flex items-center justify-between gap-2 {attributes?.done &&
				attributes?.done !== 'true' &&
				!messageDone
					? 'shimmer'
					: ''}
			"
			>
				{#if attributes?.done && attributes?.done !== 'true' && !messageDone}
					<div>
						<Spinner className="size-4" />
					</div>
				{/if}

				<div class="">
					{#if attributes?.type === 'reasoning'}
						{#if (attributes?.done === 'true' || messageDone) && attributes?.duration}
							{#if attributes.duration < 1}
								{$i18n.t('Thought for less than a second')}
							{:else if attributes.duration < 60}
								{$i18n.t('Thought for {{DURATION}} seconds', {
									DURATION: attributes.duration
								})}
							{:else}
								{$i18n.t('Thought for {{DURATION}}', {
									DURATION: dayjs.duration(attributes.duration, 'seconds').humanize()
								})}
							{/if}
						{:else if attributes?.done === 'true' || messageDone}
							{$i18n.t('Thought')}
						{:else}
							{$i18n.t('Thinking...')}
						{/if}
					{:else if attributes?.type === 'code_interpreter'}
						{#if attributes?.done === 'true' || messageDone}
							{$i18n.t('Analyzed')}
						{:else}
							{$i18n.t('Analyzing...')}
						{/if}
					{:else}
						{title}
					{/if}
				</div>

				{#if !disabled}
					<div class="flex self-center translate-y-[1px]">
						{#if open}
							<ChevronUp strokeWidth="3.5" className="size-3.5" />
						{:else}
							<ChevronDown strokeWidth="3.5" className="size-3.5" />
						{/if}
					</div>
				{/if}
			</div>
		</div>
	{:else}
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			class="{buttonClassName} cursor-pointer"
			on:click={(e) => {
				e.stopPropagation();
			}}
			on:pointerup={(e) => {
				if (!disabled) {
					open = !open;
				}
			}}
		>
			<div>
				<div class="flex items-start justify-between">
					<slot />

					{#if chevron}
						<div class="flex self-start translate-y-1">
							{#if open}
								<ChevronUp strokeWidth="3.5" className="size-3.5" />
							{:else}
								<ChevronDown strokeWidth="3.5" className="size-3.5" />
							{/if}
						</div>
					{/if}

					<div class="flex items-center gap-1.5">
						{#if attributes?.type === 'reasoning'}
							<!-- Chevron -->
							<div class="text-gray-400 dark:text-gray-500 transition-transform duration-200 {open ? 'rotate-90' : ''}">
								<ChevronRight className="size-3" />
							</div>
							<!-- Lightbulb Icon -->
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-4 text-purple-700 dark:text-purple-700">
								<path d="M12 .75a8.25 8.25 0 0 0-4.135 15.39c.686.398 1.115 1.008 1.134 1.623a.75.75 0 0 0 .75.737h4.502a.75.75 0 0 0 .75-.737c.02-.615.448-1.225 1.134-1.623A8.25 8.25 0 0 0 12 .75Z"/>
								<path fill-rule="evenodd" d="M9.013 19.9a.75.75 0 0 1 .877-.597 11.319 11.319 0 0 0 4.22 0 .75.75 0 1 1 .28 1.473 12.819 12.819 0 0 1-4.78 0 .75.75 0 0 1-.597-.876ZM9.754 22.344a.75.75 0 0 1 .824-.668 13.682 13.682 0 0 0 2.844 0 .75.75 0 1 1 .156 1.492 15.156 15.156 0 0 1-3.156 0 .75.75 0 0 1-.668-.824Z" clip-rule="evenodd"/>
							</svg>
							<span class="text-sm font-medium text-purple-700 dark:text-purple-700">
								{#if attributes?.done === 'true' && attributes?.duration}
									{#if attributes.duration < 1}
										{$i18n.t('Thought for less than a second')}
									{:else if attributes.duration < 60}
										{$i18n.t('Thought for {{DURATION}} seconds', {
											DURATION: attributes.duration
										})}
									{:else}
										{$i18n.t('Thought for {{DURATION}}', {
											DURATION: dayjs.duration(attributes.duration, 'seconds').humanize()
										})}
									{/if}
								{:else}
								<span class="shimmer">{$i18n.t('Thinking...')}</span>
							{/if}
						</span>
						{:else if attributes?.type === 'code_interpreter'}

							{#if attributes?.done === 'true'}
								{$i18n.t('Analyzed')}
							{:else}
								{$i18n.t('Analyzing...')}
							{/if}
						{:else}
							{title}
						{/if}
					</div>

					{#if attributes?.type !== 'reasoning'}
						<div class="flex self-center translate-y-[1px]">
							{#if open}
								<ChevronUp strokeWidth="3.5" className="size-3.5" />
							{:else}
								<ChevronDown strokeWidth="3.5" className="size-3.5" />
							{/if}
						</div>
					{/if}
				</div>

				{#if grow}
					{#if open && !hide}
						<div
							transition:slide={{ duration: 300, easing: quintOut, axis: 'y' }}
							on:pointerup={(e) => {
								e.stopPropagation();
							}}
						>
							<slot name="content" />
						</div>
					{/if}
				{/if}
			</div>
		</div>
	{/if}

	{#if !grow}
		{#if open && !hide}
			<div transition:slide={{ duration: 300, easing: quintOut, axis: 'y' }}>
				<slot name="content" />
			</div>
		{/if}
	{/if}
</div>

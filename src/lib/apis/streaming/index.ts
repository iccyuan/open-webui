import { EventSourceParserStream } from 'eventsource-parser/stream';
import type { ParsedEvent } from 'eventsource-parser';

type TextStreamUpdate = {
	done: boolean;
	value: string;
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	sources?: any;
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	selectedModelId?: any;
	error?: any;
	usage?: ResponseUsage;
};

type ResponseUsage = {
	/** Including images and tools if any */
	prompt_tokens: number;
	/** The tokens generated */
	completion_tokens: number;
	/** Sum of the above two fields */
	total_tokens: number;
	/** Any other fields that aren't part of the base OpenAI spec */
	[other: string]: unknown;
};

// createOpenAITextStream takes a responseBody with a SSE response,
// and returns an async generator that emits delta updates with large deltas chunked into random sized chunks
export async function createOpenAITextStream(
	responseBody: ReadableStream<Uint8Array>,
	splitLargeDeltas: boolean
): Promise<AsyncGenerator<TextStreamUpdate>> {
	const eventStream = responseBody
		.pipeThrough(new TextDecoderStream())
		.pipeThrough(new EventSourceParserStream())
		.getReader();
	let iterator = openAIStreamToIterator(eventStream);
	if (splitLargeDeltas) {
		iterator = streamLargeDeltasAsRandomChunks(iterator);
	}
	return iterator;
}

async function* openAIStreamToIterator(
	reader: ReadableStreamDefaultReader<ParsedEvent>
): AsyncGenerator<TextStreamUpdate> {
	while (true) {
		const { value, done } = await reader.read();
		if (done) {
			yield { done: true, value: '' };
			break;
		}
		if (!value) {
			continue;
		}
		const data = value.data;
		if (data.startsWith('[DONE]')) {
			yield { done: true, value: '' };
			break;
		}

		try {
			const parsedData = JSON.parse(data);
			console.log(parsedData);

			if (parsedData.error) {
				yield { done: true, value: '', error: parsedData.error };
				break;
			}

			if (parsedData.sources) {
				yield { done: false, value: '', sources: parsedData.sources };
				continue;
			}

			if (parsedData.selected_model_id) {
				yield { done: false, value: '', selectedModelId: parsedData.selected_model_id };
				continue;
			}

			if (parsedData.usage) {
				yield { done: false, value: '', usage: parsedData.usage };
				continue;
			}

			yield {
				done: false,
				value: parsedData.choices?.[0]?.delta?.content ?? ''
			};
		} catch (e) {
			console.error('Error extracting delta from SSE event:', e);
		}
	}
}

// Advanced typewriter animation with actual character width measurement
// Uses Canvas API to measure real rendered width for optimal chunking
async function* streamLargeDeltasAsRandomChunks(
	iterator: AsyncGenerator<TextStreamUpdate>
): AsyncGenerator<TextStreamUpdate> {
	// Canvas-based character width measurement (cached for performance)
	const widthCache = new Map<string, number>();
	let canvas: HTMLCanvasElement | null = null;
	let ctx: CanvasRenderingContext2D | null = null;

	const getCharacterWidth = (char: string): number => {
		// Check cache first
		if (widthCache.has(char)) {
			return widthCache.get(char)!;
		}

		// Lazy initialize canvas
		if (!canvas) {
			canvas = document.createElement('canvas');
			ctx = canvas.getContext('2d');
			if (ctx) {
				// Use a common font for measurement
				ctx.font = '16px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
			}
		}

		if (!ctx) {
			// Fallback: estimate based on byte length
			return new Blob([char]).size;
		}

		// Measure actual width
		const metrics = ctx.measureText(char);
		const width = metrics.width;

		// Cache the result
		widthCache.set(char, width);

		return width;
	};

	// Get optimal chunk based on actual rendered width
	const getOptimalChunk = (content: string): string => {
		const TARGET_WIDTH = 80; // Target pixel width (adjustable)
		let currentWidth = 0;
		let chunkEnd = 0;

		for (let i = 0; i < content.length; i++) {
			const char = content[i];
			const charWidth = getCharacterWidth(char);

			if (currentWidth + charWidth > TARGET_WIDTH && chunkEnd > 0) {
				break;
			}

			currentWidth += charWidth;
			chunkEnd = i + 1;
		}

		return content.slice(0, Math.max(1, chunkEnd));
	};

	// Smart delay based on punctuation and content type
	const getSmartDelay = (chunk: string): number => {
		const lastChar = chunk[chunk.length - 1];

		// Sentence endings - longer pause for natural reading rhythm
		if (lastChar.match(/[。！？.!?]/)) return 80;

		// Commas - medium pause
		if (lastChar.match(/[，,、]/)) return 30;

		// Semicolons and colons
		if (lastChar.match(/[；;：:]/)) return 40;

		// Line breaks - noticeable pause
		if (lastChar === '\n') return 50;

		// Code-like content (fast)
		if (chunk.match(/^[a-zA-Z0-9_\-+={}[\]()<>\/\\|&*^%$#@!~`'"]+$/)) return 1;

		// Default - smooth and fast
		return 2;
	};

	for await (const textStreamUpdate of iterator) {
		if (textStreamUpdate.done) {
			yield textStreamUpdate;
			return;
		}
		if (textStreamUpdate.error) {
			yield textStreamUpdate;
			continue;
		}
		if (textStreamUpdate.sources) {
			yield textStreamUpdate;
			continue;
		}
		if (textStreamUpdate.selectedModelId) {
			yield textStreamUpdate;
			continue;
		}
		if (textStreamUpdate.usage) {
			yield textStreamUpdate;
			continue;
		}

		let content = textStreamUpdate.value;

		// Short content - output directly
		if (content.length < 3) {
			yield { done: false, value: content };
			continue;
		}

		// Smart chunking with width-based optimization
		while (content.length > 0) {
			const chunk = getOptimalChunk(content);
			yield { done: false, value: chunk };

			// Smart delay with punctuation awareness
			// Do not sleep if the tab is hidden (timers are throttled to 1s)
			if (document?.visibilityState !== 'hidden') {
				await sleep(getSmartDelay(chunk));
			}

			content = content.slice(chunk.length);
		}
	}
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

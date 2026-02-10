import type { TransitionConfig } from 'svelte/transition';

type FlyAndScaleParams = {
	y?: number;
	start?: number;
	duration?: number;
};

// Apple-style spring easing: gentle overshoot then settle
export const appleSpring = (t: number): number => {
	const s = 1.2;
	const t1 = t - 1;
	return t1 * t1 * ((s + 1) * t1 + s) + 1;
};

const defaultFlyAndScaleParams = { y: -6, start: 0.97, duration: 300 };

export const flyAndScale = (node: Element, params?: FlyAndScaleParams): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === 'none' ? '' : style.transform;
	const withDefaults = { ...defaultFlyAndScaleParams, ...params };

	const scaleConversion = (valueA: number, scaleA: [number, number], scaleB: [number, number]) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (style: Record<string, number | string | undefined>): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, '');
	};

	return {
		duration: withDefaults.duration ?? 300,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [withDefaults.y, 0]);
			const scale = scaleConversion(t, [0, 1], [withDefaults.start, 1]);

			return styleToString({
				transform: `${transform} translate3d(0, ${y}px, 0) scale(${scale})`,
				opacity: Math.min(1, t * 1.5)
			});
		},
		easing: appleSpring
	};
};

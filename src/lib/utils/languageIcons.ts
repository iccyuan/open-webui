/**
 * Inline SVG icons for programming languages.
 * Hand-crafted clean icons based on official logos, optimised for 14px display.
 * All icons use viewBox="0 0 16 16" for crisp pixel-level rendering.
 */
export const LANGUAGE_ICONS: Record<string, string> = {
	// ── JavaScript ── yellow floating badge (inset, not full-bleed)
	javascript: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" fill="#F7DF1E"/><text x="3.5" y="12" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="#000">JS</text></svg>`,

	// ── TypeScript ── blue floating badge (inset, not full-bleed)
	typescript: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" fill="#3178C6"/><text x="3.5" y="12" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="#fff">TS</text></svg>`,

	// ── Python ── interlinked snake shapes (blue + yellow)
	python: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M8 1.5C5.5 1.5 4 2.6 4 4v2.5h4v1H3C1.5 7.5 1 8.5 1 10s.7 2.5 2 2.5h1V11c0-1 .7-1.5 2-1.5h4c1.2 0 2-.7 2-2V4c0-1.3-1.5-2.5-4-2.5zm-1 2a.75.75 0 1 1 0 1.5A.75.75 0 0 1 7 3.5z" fill="#3776AB"/><path d="M8 14.5c2.5 0 4-1.1 4-2.5V9.5H8v-1h5c1.5 0 2-1 2-2.5s-.7-2.5-2-2.5h-1V5c0 1-.7 1.5-2 1.5H6c-1.2 0-2 .7-2 2v2.5c0 1.3 1.5 2.5 4 2.5zm1-2a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5z" fill="#FFD43B"/></svg>`,

	// ── HTML5 ── orange shield with white H
	html: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M2 1l1.2 13L8 15.5 12.8 14 14 1H2z" fill="#E34F26"/><path d="M8 14.3V2.5h4.7l-1 10.7L8 14.3z" fill="#EF652A"/><path d="M5.5 5.5h5l-.2 2H6l.2 1.8h3.9l-.3 3.2L8 13l-1.8-.5-.1-1.5H7.3l.05.8.65.17.65-.17.07-.85-.05.06H5.7L5.5 5.5z" fill="#fff"/></svg>`,

	// ── CSS3 ── purple shield (same structure as HTML5, purple palette)
	css: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M2 1l1.2 13L8 15.5 12.8 14 14 1H2z" fill="#663399"/><path d="M8 14.3V2.5h4.7l-1 10.7L8 14.3z" fill="#8545C7"/><path d="M5.5 5.5h5l-.2 2H6l.2 1.8h3.9l-.3 3.2L8 13l-1.8-.5-.1-1.5H7.3l.05.8.65.17.65-.17.07-.85-.05.06H5.7L5.5 5.5z" fill="#fff"/></svg>`,

	// ── Sass/SCSS ── pink circle
	scss: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7.5" fill="#CC6699"/><path d="M5 10.2c.5-.2 1.1-.5 1.8-.8.2.4.4.7.8.9.6.3 1.3.1 1.9-.5.7-.8.4-1.8-.1-2.4-.6-.6-1.7-1-1.9-1.9-.1-.8.5-1.5 1.3-1.6.7-.1 1.3.3 1.7.9l-1 .7c-.1-.3-.4-.5-.7-.4-.3 0-.5.3-.4.6.1.5 1 .9 1.6 1.5.9.9 1 2.4.1 3.3-.9 1-2.3 1.3-3.4.8-.6-.3-1-.8-1.2-1.4z" fill="#fff"/></svg>`,

	// ── React ── cyan atom
	react: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="8" rx="6.5" ry="2.5" stroke="#61DAFB" stroke-width="1.2"/><ellipse cx="8" cy="8" rx="6.5" ry="2.5" stroke="#61DAFB" stroke-width="1.2" transform="rotate(60 8 8)"/><ellipse cx="8" cy="8" rx="6.5" ry="2.5" stroke="#61DAFB" stroke-width="1.2" transform="rotate(120 8 8)"/><circle cx="8" cy="8" r="1.5" fill="#61DAFB"/></svg>`,

	// ── Vue.js ── green chevron V
	vue: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M1 2h2.2L8 10.5 12.8 2H15L8 14.5 1 2z" fill="#42B883"/><path d="M5.5 2h2L8 5l.5-3h2L8 10.5 5.5 2z" fill="#35495E"/></svg>`,

	// ── Svelte ── orange S
	svelte: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M12.5 3.5C11 1.5 8 1 5.5 2.5L3 4.5C1 6 1.5 8.5 2.5 9.5c-.5.7-.7 1.7-.3 2.5.5 1 1.5 1.5 2.5 1.5.5 0 1-.1 1.5-.5l2.5-2c2-1.5 1.5-4-.5-4.5.3-.3.6-.8.5-1.3-.1-.5-.5-.8-.9-1-.7-.3-1.5-.1-2 .3l-1.5 1.2c-.5.4-.5 1 0 1.3.4.3 1 .2 1.4-.1L7 6.2c.2-.2.5-.2.7 0 .2.2.1.5-.1.7L5 8.7c-.8.7-2 .5-2.5-.4-.4-.8 0-1.8.8-2.2l2.5-2C7 3 9 3.5 9.8 5c.4.8.2 1.8-.5 2.3.7.2 1.1.9 1 1.7-.1.5-.5 1-.9 1.3l-2.5 2c-.5.4-1 .5-1.5.5.6.3 1.3.3 2 .1l2.5-1.5c2-1.2 2.5-4 1.6-5.9" stroke="#FF3E00" stroke-width="1.2" stroke-linecap="round"/></svg>`,

	// ── Angular ── red A shield
	angular: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M8 1L2 3.5l1 8.5 5 3 5-3 1-8.5L8 1z" fill="#DD0031"/><path d="M8 1v13.5l5-3 1-8.5L8 1z" fill="#C3002F"/><path d="M8 3.5L5.5 10h1l.5-1.5h2l.5 1.5h1L8 3.5zm0 2l.7 2H7.3L8 5.5z" fill="#fff"/></svg>`,

	// ── GraphQL ── pink hexagon
	graphql: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><polygon points="8,2 13.5,5.5 13.5,10.5 8,14 2.5,10.5 2.5,5.5" stroke="#E10098" stroke-width="1.3"/><circle cx="8" cy="2" r="1.3" fill="#E10098"/><circle cx="13.5" cy="5.5" r="1.3" fill="#E10098"/><circle cx="13.5" cy="10.5" r="1.3" fill="#E10098"/><circle cx="8" cy="14" r="1.3" fill="#E10098"/><circle cx="2.5" cy="10.5" r="1.3" fill="#E10098"/><circle cx="2.5" cy="5.5" r="1.3" fill="#E10098"/></svg>`,

	// ── Go ── teal floating badge (inset, not full-bleed)
	go: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" fill="#00ADD8"/><text x="3" y="12" font-family="Arial,sans-serif" font-size="8.5" font-weight="bold" fill="#fff">Go</text></svg>`,

	// ── Rust ── gear wheel
	rust: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="3" stroke="#CE422B" stroke-width="1.4"/><circle cx="8" cy="8" r="5.5" stroke="#CE422B" stroke-width="1.1"/><path d="M8 1.5V2.5M8 13.5V14.5M1.5 8H2.5M13.5 8H14.5M3.2 3.2l.7.7M12.1 12.1l.7.7M12.8 3.2l-.7.7M3.9 12.1l-.7.7" stroke="#CE422B" stroke-width="1.3" stroke-linecap="round"/></svg>`,

	// ── Java ── orange coffee cup
	java: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M5 5c.5-1 .5-1.5 0-2.5" stroke="#5382A1" stroke-width="1.2" stroke-linecap="round"/><path d="M7.5 4.5C8 3.5 8 3 7.5 2" stroke="#F89820" stroke-width="1.2" stroke-linecap="round"/><rect x="3" y="6.5" width="8" height="5.5" rx="1.5" stroke="#5382A1" stroke-width="1.2"/><path d="M11 8.5h1.5a1 1 0 0 1 0 2H11" stroke="#5382A1" stroke-width="1.2" stroke-linecap="round"/><path d="M2.5 14h11" stroke="#5382A1" stroke-width="1.2" stroke-linecap="round"/></svg>`,

	// ── Kotlin ── purple/orange K triangle
	kotlin: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><defs><linearGradient id="kg" x1="0" y1="0" x2="16" y2="16" gradientUnits="userSpaceOnUse"><stop stop-color="#E44857"/><stop offset="0.5" stop-color="#C711E1"/><stop offset="1" stop-color="#7F52FF"/></linearGradient></defs><path d="M1 1h7L1 8.5V1zM8 1L1 15h7L15 1H8zM15 15L8 8l7 7z" fill="url(#kg)"/></svg>`,

	// ── Swift ── orange rounded badge (inset) with bird swoosh
	swift: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="1.5" y="1.5" width="13" height="13" rx="3" fill="#F05138"/><path d="M12 4.5C10.5 3 8 2.8 5.5 4.5L3.5 6c1.5 1 3.5 2 5 1.5C7 8.5 5 7.5 4 6.5c1.5 1.5 3.5 3 6 2.5-.5.5-1 1-1.5 1.5H11c.5-.5 1-1.5 1-2.5 0-.5-.3-1-.5-1.5l1.5.5z" fill="#fff"/></svg>`,

	// ── C ── blue circle with white C-arc stroke
	c: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#5C6BC0"/><path d="M11.5 4.5A5 5 0 1 0 11.5 11.5" stroke="#fff" stroke-width="1.9" stroke-linecap="round" fill="none"/></svg>`,

	// ── C++ ── dark blue circle with C-arc + plus signs
	cpp: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#00599C"/><path d="M9.5 4.5A4 4 0 1 0 9.5 11.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none"/><path d="M12 5.5v2.5M10.75 6.75h2.5" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/><path d="M12 9v2.5M10.75 10.25h2.5" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/></svg>`,

	// ── C# ── purple circle with C-arc + hash lines
	csharp: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#68217A"/><path d="M9 4.5A4 4 0 1 0 9 11.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none"/><path d="M11 5.5v5M12.5 5.5v5M10.2 7.5h3.1M10.2 9.5h3.1" stroke="#fff" stroke-width="1" stroke-linecap="round"/></svg>`,

	// ── Scala ── red stacked bars
	scala: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="3" width="12" height="3" rx="0.5" fill="#DC322F"/><rect x="2" y="7.5" width="12" height="3" rx="0.5" fill="#DC322F" opacity="0.7"/><rect x="2" y="12" width="12" height="3" rx="0.5" fill="#DC322F" opacity="0.4"/></svg>`,

	// ── PHP ── indigo ellipse badge
	php: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><ellipse cx="8" cy="8" rx="7" ry="5" fill="#777BB4"/><text x="2.5" y="11.5" font-family="Arial,sans-serif" font-size="7.5" font-weight="bold" fill="#fff">php</text></svg>`,

	// ── Ruby ── red gem
	ruby: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M5 2h6l3.5 4-6.5 9L2 6 5 2z" fill="#CC342D"/><path d="M2 6l4.5 1L8 15 2 6z" fill="#a01f1a"/><path d="M14 6L9.5 7 8 15l6-9z" fill="#c43a30"/><path d="M5 2l3 5 3-5H5z" fill="#e06565"/><path d="M2 6l3-4 3 5L2 6z" fill="#e06565" opacity="0.6"/></svg>`,

	// ── Lua ── blue circle badge
	lua: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#000080"/><circle cx="12" cy="4" r="2.5" fill="#000080" stroke="#fff" stroke-width="1"/><text x="3" y="12" font-family="Arial,sans-serif" font-size="7" font-weight="bold" fill="#fff">Lua</text></svg>`,

	// ── Perl ── purple
	perl: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#39457E"/><text x="3" y="12" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#fff">Pl</text></svg>`,

	// ── Dart ── blue dart-shaped badge
	dart: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M3 8.5L6 3h4.5L14 6.5 9 14H5L3 8.5z" fill="#0175C2"/><path d="M3 8.5L6 3 3 6.5v2z" fill="#03589C"/><circle cx="5.5" cy="13" r="1.5" fill="#03589C"/></svg>`,

	// ── Haskell ── purple lambda
	haskell: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M1 13L5.5 8 1 3h2l4.5 5L3 13H1z" fill="#5D4F85"/><path d="M5 13L9.5 8 5 3h2l4.5 5L7 13H5z" fill="#8F4E8B"/><path d="M11 10l-1.5-2h4.5l1 1-1 1H11zM9 7.5L7.5 5.5H12l1 1-1 1H9z" fill="#8F4E8B"/></svg>`,

	// ── Elixir ── purple water drop
	elixir: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M8 2C8 2 3 7 3 10.5a5 5 0 0 0 10 0C13 7 8 2 8 2z" fill="#4B275F"/><path d="M8 2C8 2 5 7 5 10.5c0 1.5.6 2.8 1.6 3.7" stroke="#8B60A1" stroke-width="1" fill="none" opacity="0.5"/></svg>`,

	// ── Erlang ── red badge
	erlang: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#A90533"/><text x="2" y="12" font-family="Arial,sans-serif" font-size="7" font-weight="bold" fill="#fff">erl</text></svg>`,

	// ── Bash ── dark terminal with >_
	bash: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M2 4.5l5 4-5 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><line x1="9" y1="12.5" x2="15" y2="12.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>`,

	// ── PowerShell ── dark navy floating badge (inset) with PS terminal mark
	powershell: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" fill="#012456"/><path d="M3 10l3.5-3.5L3 3" stroke="#00B5F5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="8" y1="10" x2="13" y2="10" stroke="#00B5F5" stroke-width="1.5" stroke-linecap="round"/></svg>`,

	// ── Docker ── blue whale
	docker: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="1" y="7.5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><rect x="3.6" y="7.5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><rect x="6.2" y="7.5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><rect x="3.6" y="5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><rect x="6.2" y="5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><rect x="8.8" y="7.5" width="2.2" height="2" rx="0.4" fill="#2496ED"/><path d="M11 9.5c1-.1 3-.7 2.5-3a2.8 2.8 0 0 0-1.5-.8s-.2-1.5-1.8-1.8" stroke="#2496ED" stroke-width="1" stroke-linecap="round"/><path d="M.5 9.5S1 13 4.5 13h7c2 0 2.5-2 2.5-2" stroke="#2496ED" stroke-width="1" stroke-linecap="round"/></svg>`,

	// ── Kubernetes ── blue hex wheel
	kubernetes: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="#326CE5" stroke-width="1.3"/><circle cx="8" cy="8" r="2.5" fill="#326CE5"/><line x1="8" y1="2" x2="8" y2="4.5" stroke="#326CE5" stroke-width="1.3"/><line x1="8" y1="11.5" x2="8" y2="14" stroke="#326CE5" stroke-width="1.3"/><line x1="2" y1="8" x2="4.5" y2="8" stroke="#326CE5" stroke-width="1.3"/><line x1="11.5" y1="8" x2="14" y2="8" stroke="#326CE5" stroke-width="1.3"/></svg>`,

	// ── Terraform ── purple stacked diamonds
	terraform: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M7 2.5L11 5v5L7 7.5V2.5z" fill="#7B42BC"/><path d="M11.5 2.5L15 5v5l-3.5-2.5V2.5z" fill="#7B42BC" opacity="0.7"/><path d="M1 5.5L4.5 3v4.5L1 10V5.5z" fill="#7B42BC" opacity="0.5"/><path d="M7 10L11 12.5v4L7 14V10z" fill="#7B42BC" opacity="0.6"/></svg>`,

	// ── Node.js ── green hex
	nodejs: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M8 1L14 4.5v7L8 15 2 11.5v-7L8 1z" fill="#339933"/><text x="3.5" y="11.5" font-family="Arial,sans-serif" font-size="5.5" font-weight="bold" fill="#fff">node</text></svg>`,

	// ── npm ── red floating badge (inset) with official npm N pattern
	npm: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="1.5" fill="#CB3837"/><rect x="3.5" y="5" width="9" height="6.5" rx="0.5" fill="#fff"/><rect x="5" y="6.5" width="1.5" height="3" fill="#CB3837"/><rect x="7.8" y="6.5" width="1.5" height="5" fill="#CB3837"/><rect x="10.5" y="6.5" width="1.5" height="3" fill="#CB3837"/></svg>`,

	// ── Deno ── black/white circle
	deno: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" fill="#fff" stroke="#000" stroke-width="1"/><circle cx="8" cy="8" r="3" fill="#000"/><circle cx="8" cy="8" r="1.2" fill="#fff"/></svg>`,

	// ── Bun ── cream/tan bun
	bun: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="9.5" rx="6.5" ry="5" fill="#FBF0DF" stroke="#F6DECE" stroke-width="0.8"/><ellipse cx="5.5" cy="5.5" rx="2" ry="2.5" fill="#FBF0DF" stroke="#F6DECE" stroke-width="0.8"/><ellipse cx="10.5" cy="5.5" rx="2" ry="2.5" fill="#FBF0DF" stroke="#F6DECE" stroke-width="0.8"/><ellipse cx="5.5" cy="9.5" rx="1.5" ry="1" fill="#00000026"/><ellipse cx="10.5" cy="9.5" rx="1.5" ry="1" fill="#00000026"/></svg>`,

	// ── PostgreSQL ── dark blue drum
	postgresql: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="5" rx="6" ry="2.5" fill="#336791"/><rect x="2" y="5" width="12" height="6" fill="#336791"/><ellipse cx="8" cy="11" rx="6" ry="2.5" fill="#4A90D9" opacity="0.7"/><ellipse cx="8" cy="5" rx="6" ry="2.5" fill="#6BA3D6" opacity="0.5"/></svg>`,

	// ── MySQL ── DB cylinder with orange-tinted top (distinct from PostgreSQL blue)
	mysql: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="5" rx="5.5" ry="2" fill="#00618A"/><rect x="2.5" y="5" width="11" height="6" fill="#00618A"/><ellipse cx="8" cy="11" rx="5.5" ry="2" fill="#0A7CB8" opacity="0.8"/><ellipse cx="8" cy="5" rx="5.5" ry="2" fill="#F29111" opacity="0.55"/><path d="M12 3c1.5-.3 2.5.7 2.5 1.8" stroke="#F29111" stroke-width="1.2" stroke-linecap="round"/></svg>`,

	// ── MongoDB ── green leaf
	mongodb: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M8 1.5C8 1.5 2 7 2 11a6 6 0 0 0 12 0C14 7 8 1.5 8 1.5z" fill="#4DB33D"/><line x1="8" y1="1.5" x2="8" y2="14.5" stroke="#3FA037" stroke-width="2"/></svg>`,

	// ── Redis ── red cylinder
	redis: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="12" rx="6" ry="2.5" fill="#A51F17"/><rect x="2" y="7" width="12" height="5" fill="#D82C20"/><ellipse cx="8" cy="7" rx="6" ry="2.5" fill="#FF6B6B"/><path d="M4 8h2l1 1.5 1.5-3 1.5 3L11 8h2" stroke="#fff" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/></svg>`,

	// ── JSON ── curly brace shape (amber, universal JSON symbol)
	json: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M6.5 3c-1 0-1.5.5-1.5 1.5V6.5L3.5 8l1.5 1.5V11.5c0 1 .5 1.5 1.5 1.5" stroke="#CE9178" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.5 3c1 0 1.5.5 1.5 1.5V6.5L12.5 8 11 9.5V11.5c0 1-.5 1.5-1.5 1.5" stroke="#CE9178" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,

	// ── YAML ── red document with horizontal lines
	yaml: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="3" y="2" width="10" height="12.5" rx="1.5" stroke="#CB171E" stroke-width="1.3"/><path d="M5.5 5.5h5M5.5 8h5M5.5 10.5h3" stroke="#CB171E" stroke-width="1.1" stroke-linecap="round"/></svg>`,

	// ── Markdown ── blue MD badge
	markdown: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="0.7" y="3" width="14.6" height="10" rx="2" stroke="#083fa1" stroke-width="1.2"/><path d="M3 11V5l2.5 3L8 5v6" stroke="#fff" fill="none" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 11V5M9 8l2 3 2-3" stroke="#fff" fill="none" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round"/></svg>`,

	// ── LaTeX ── teal document with formula hint (dog-ear corner)
	latex: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M3 2h7.5L13 4.5V14H3V2z" stroke="#008080" stroke-width="1.3" stroke-linejoin="round"/><path d="M10.5 2v2.5H13" stroke="#008080" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/><path d="M5.5 7h5M5.5 9.5h3.5M5.5 12h4.5" stroke="#008080" stroke-width="1" stroke-linecap="round"/></svg>`,

	// ── Jupyter ── orange circles
	jupyter: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="4" r="2.5" fill="#F37726"/><circle cx="13" cy="11" r="2.5" fill="#F37726"/><circle cx="3" cy="11" r="2.5" fill="#F37726"/><circle cx="8" cy="8" r="2.5" fill="#4e4e4e"/></svg>`,

	// ── Solidity ── grey hexagon
	solidity: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><polygon points="8,2 13.5,5 13.5,11 8,14 2.5,11 2.5,5" fill="#383838"/><polygon points="8,2 13.5,5 13.5,11 8,14 2.5,11 2.5,5" fill="#2B6AFF" opacity="0.45"/></svg>`,

	// ── Vite ── purple/blue lightning
	vite: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><defs><linearGradient id="vg" x1="0" y1="0" x2="16" y2="16"><stop stop-color="#41D1FF"/><stop offset="1" stop-color="#BD34FE"/></linearGradient></defs><path d="M14 2.5L8 9.5l1-5L2 13.5L8 6.5l-1 5L14 2.5z" fill="url(#vg)"/></svg>`,

	// ── Webpack ── blue hex
	webpack: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><polygon points="8,1 14,4.5 14,11.5 8,15 2,11.5 2,4.5" fill="#8DD6F9"/><polygon points="8,1 14,4.5 14,11.5 8,15" fill="#1C78C0"/><path d="M8 5v6M5 6.5l3 2L5 10M11 6.5L8 8.5l3 1.5" stroke="#fff" stroke-width="1" stroke-linecap="round"/></svg>`,

	// ── Jest ── red circle with exclamation
	jest: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#C21325"/><rect x="7.2" y="4" width="1.6" height="5" rx="0.5" fill="#fff"/><circle cx="8" cy="11.5" r="1" fill="#fff"/></svg>`,

	// ── ESLint ── purple hex
	eslint: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><polygon points="8,2 13.5,5 13.5,11 8,14 2.5,11 2.5,5" stroke="#4B32C3" stroke-width="1.2"/><polygon points="8,5.5 11,7.5 11,11 8,12.5 5,11 5,7.5" fill="#4B32C3"/></svg>`,

	// ── Firebase ── orange flame
	firebase: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M4 13.5L5.5 5l3 4 1.5-7 4 12H4z" fill="#FFA000"/><path d="M4 13.5L5.5 5 7.5 9.5 4 13.5z" fill="#F57F17"/><path d="M10 2l5.5 11.5H4L10 2z" fill="#FFCA28"/></svg>`,

	// ── Supabase ── green lightning bolt
	supabase: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><defs><linearGradient id="sg" x1="0" y1="0" x2="16" y2="16"><stop stop-color="#3ECF8E"/><stop offset="1" stop-color="#1C9C6B"/></linearGradient></defs><path d="M9 1.5v7h5.5L7 14.5V7.5H1.5L9 1.5z" fill="url(#sg)"/></svg>`,

	// ── Gradle ── dark green curves
	gradle: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M3.5 12C3.5 12 8 5 14 5" stroke="#02303A" stroke-width="2.5" stroke-linecap="round"/><path d="M3.5 14.5C3.5 14.5 9 7 15 9" stroke="#02303A" stroke-width="2" stroke-linecap="round"/><circle cx="14" cy="5" r="2" fill="#02303A"/></svg>`,

	// ── Nginx ── green badge
	nginx: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M8 1L14 5v6l-6 4L2 11V5L8 1z" fill="#009900"/><text x="3.5" y="12" font-family="Arial,sans-serif" font-size="5" font-weight="bold" fill="#fff">nginx</text></svg>`,

	// ── R ── blue badge
	r: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><ellipse cx="8" cy="7.5" rx="6" ry="5.5" fill="#276DC3" stroke="#75AADB" stroke-width="0.8"/><text x="4.5" y="11" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#fff">R</text><path d="M8.5 9.5l4 5" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>`,

	// ── WebAssembly ── purple box with W waveform path
	wasm: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="1.5" fill="#654FF0"/><path d="M4.5 5l1.5 7 2-4.5 2 4.5 1.5-7" stroke="#fff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>`,

	// ── Sass ── pink circle Ss
	sass: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#CC6699"/><text x="3" y="12" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="#fff">Ss</text></svg>`,

	// ── Less ── dark navy circle with white Less L-dot mark
	less: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" fill="#1D365D"/><path d="M5.5 4v7.5h5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="5" r="1.2" fill="#3B82F6"/></svg>`,

	// ── OCaml ── orange badge
	ocaml: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#EE6A1A"/><text x="2" y="12" font-family="Arial,sans-serif" font-size="7" font-weight="bold" fill="#fff">ML</text></svg>`,

	// ── Crystal ── faceted gem
	crystal: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><polygon points="8,2 13,6 13,11 8,15 3,11 3,6" fill="#888"/><polygon points="8,2 13,6 8,9" fill="#ccc"/><polygon points="3,6 8,9 8,2" fill="#555"/><polygon points="8,9 13,11 8,15" fill="#aaa"/><polygon points="8,9 3,11 8,15" fill="#777"/></svg>`,

	// ── Julia ── three colored circles
	julia: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="6" cy="6" r="4" fill="#389826"/><circle cx="10" cy="6" r="4" fill="#CB3C33"/><circle cx="8" cy="10" r="4" fill="#9558B2"/></svg>`,

	// ── NixOS ── snowflake / lambda blue
	nix: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M8 2l2 3.5h-4L8 2zM8 14l-2-3.5h4L8 14zM2 5.5l3.5 0L4 9 2 5.5zM14 10.5L10.5 10.5 12 7 14 10.5z" fill="#5277C3"/><path d="M2 10.5l1.5-2.5L4 9.5l-2 1zM14 5.5l-1.5 2.5L12 6.5l2-1z" fill="#7EBAE4"/></svg>`,

	// ── Helm ── navy wheel
	helm: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" fill="#0F1689"/><circle cx="8" cy="8" r="3" stroke="#fff" stroke-width="1.2"/><line x1="8" y1="1" x2="8" y2="4.5" stroke="#fff" stroke-width="1.2"/><line x1="8" y1="11.5" x2="8" y2="15" stroke="#fff" stroke-width="1.2"/><line x1="1" y1="8" x2="4.5" y2="8" stroke="#fff" stroke-width="1.2"/><line x1="11.5" y1="8" x2="15" y2="8" stroke="#fff" stroke-width="1.2"/></svg>`,

	// ── Ansible ── dark circle A
	ansible: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#1A1918"/><path d="M8 3l4 9-4-3-4 3 4-9z" fill="#fff"/></svg>`,

	// ── Groovy ── blue G circle
	groovy: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#4298B8"/><text x="3.5" y="12" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#fff">Gv</text></svg>`,

	// ── Clojure ── concentric circles
	clojure: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" fill="#5881D8"/><circle cx="8" cy="8" r="4.5" stroke="#fff" stroke-width="1.3"/><circle cx="8" cy="8" r="1.8" fill="#90B8F8"/></svg>`,

	// ── Zig ── golden Z lightning
	zig: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path d="M2 4.5h8l-4 3h6" stroke="#F7A41D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 11.5h8l-4-3h6" stroke="#F7A41D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="5.5" y="5.5" width="5" height="5" fill="#F7A41D"/></svg>`,

	// ── Mocha ── brown mug
	mocha: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="2.5" y="5" width="8" height="8" rx="1.5" stroke="#8D6748" stroke-width="1.3" fill="#8D6748"/><path d="M10.5 7h2a1.5 1.5 0 0 1 0 3h-2" stroke="#8D6748" stroke-width="1.3" stroke-linecap="round"/><path d="M4 3.5c.5-.5 1-1.5 0-2.5" stroke="#8D6748" stroke-width="1" stroke-linecap="round"/><path d="M7 3c.5-.5 1-1.5 0-2.5" stroke="#8D6748" stroke-width="1" stroke-linecap="round"/></svg>`,

	// ── Rollup ── orange circle with funnel
	rollup: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#EC4A25"/><path d="M4.5 6l3.5 3 3.5-3L8 4 4.5 6z" fill="#fff"/><path d="M4.5 6l3.5 3v4L4.5 6z" fill="#fff" opacity="0.7"/></svg>`,

	// ── Vitest ── yellow-green hex
	vitest: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><defs><linearGradient id="vi" x1="0" y1="0" x2="16" y2="16"><stop stop-color="#FCC72B"/><stop offset="1" stop-color="#729B1B"/></linearGradient></defs><polygon points="8,1.5 14.5,5 14.5,12 8,15.5 1.5,12 1.5,5" fill="url(#vi)"/><path d="M5 9l3 3.5 5-6" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,

	// ── CMake ── tricolor triangle
	cmake: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M8 2L15 14H8V2z" fill="#248AC2"/><path d="M8 2L1 14H8V2z" fill="#BF3B28"/><circle cx="8" cy="10.5" r="2.5" fill="#fff"/></svg>`,

	// ── Bazel ── green hex star
	bazel: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><polygon points="8,1 14,4.5 14,11.5 8,15 2,11.5 2,4.5" fill="#76D275"/><path d="M8 5v6M5 8h6M6 5.5l4 5M10 5.5l-4 5" stroke="#fff" stroke-width="0.7" opacity="0.5"/></svg>`,

	// ── Maven ── red circle mvn
	maven: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#C71A36"/><text x="3" y="12" font-family="Arial,sans-serif" font-size="6.5" font-weight="bold" fill="#fff">mvn</text></svg>`,

	// ── Matlab ── wave chart
	matlab: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M1 13L5 6l3 6.5 3-8 4 8H1z" fill="#0076A8"/><path d="M10 6l3 4-5-2 2-2z" fill="#EE2E24"/></svg>`,

	// ── Cassandra ── eye shape
	cassandra: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="8" rx="7" ry="4.5" stroke="#1287B1" stroke-width="1.3"/><circle cx="8" cy="8" r="2.5" fill="#1287B1"/><circle cx="8" cy="8" r="1" fill="#fff"/></svg>`,

	// ── Neo4j ── blue connected circles
	neo4j: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="4.5" cy="5" r="2.5" fill="#4581C3"/><circle cx="11.5" cy="5" r="2.5" fill="#4581C3"/><circle cx="8" cy="12" r="2.5" fill="#4581C3"/><line x1="4.5" y1="5" x2="11.5" y2="5" stroke="#4581C3" stroke-width="1.3"/><line x1="4.5" y1="5" x2="8" y2="12" stroke="#4581C3" stroke-width="1.3"/><line x1="11.5" y1="5" x2="8" y2="12" stroke="#4581C3" stroke-width="1.3"/></svg>`,

	// ── Elasticsearch ── teal lens
	elasticsearch: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><ellipse cx="8" cy="8" rx="6.5" ry="5.5" fill="#00BFB3"/><ellipse cx="8" cy="6" rx="4.5" ry="2.5" fill="#FEC514" opacity="0.9"/><ellipse cx="8" cy="10.5" rx="4.5" ry="2.5" fill="#FEC514" opacity="0.6"/></svg>`,

	// ── SQLite ── navy floating badge (inset) with S/QL
	sqlite: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="12" height="12" rx="2" fill="#003B57"/><text x="3.5" y="12" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#fff">S</text><text x="9.5" y="12" font-family="Arial,sans-serif" font-size="5.5" fill="#fff" opacity="0.7">QL</text></svg>`,

	// ── pnpm ── gold grid
	pnpm: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="1" y="1" width="4.5" height="4.5" rx="0.5" fill="#F9AD00"/><rect x="6" y="1" width="4.5" height="4.5" rx="0.5" fill="#F9AD00"/><rect x="11" y="1" width="4.5" height="4.5" rx="0.5" fill="#F9AD00"/><rect x="1" y="6.5" width="4.5" height="4.5" rx="0.5" fill="#F9AD00"/><rect x="6" y="6.5" width="4.5" height="4.5" rx="0.5" fill="#4E4E4E"/><rect x="11" y="6.5" width="4.5" height="4.5" rx="0.5" fill="#4E4E4E"/><rect x="1" y="12" width="4.5" height="4.5" rx="0.5" fill="#F9AD00"/><rect x="6" y="12" width="4.5" height="4.5" rx="0.5" fill="#4E4E4E"/><rect x="11" y="12" width="4.5" height="4.5" rx="0.5" fill="#4E4E4E"/></svg>`,

	// ── Yarn ── blue yarn ball
	yarn: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" fill="#2C8EBB"/><path d="M4 5c0 0 2 4.5 4 4.5s5-4 5-4" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><circle cx="4" cy="5" r="1.5" fill="#fff"/></svg>`,
};

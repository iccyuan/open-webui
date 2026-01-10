import { EditorView } from '@codemirror/view';
import { Extension } from '@codemirror/state';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { tags as t } from '@lezer/highlight';

// Dark theme colors (Antigravity)
const darkColors = {
    chalky: '#e5c07b',
    coral: '#ff7b72',
    cyan: '#79c0ff',
    invalid: '#ffffff',
    ivory: '#e6edf3',
    stone: '#8b949e',
    malibu: '#a5d6ff',
    sage: '#98c379',
    whiskey: '#ffa657',
    violet: '#d2a8ff',
    darkBackground: '#0d1117',
    highlightBackground: '#1c2128',
    background: '#0d1117',
    tooltipBackground: '#1c2128',
    selection: '#264f78',
    cursor: '#79c0ff'
};

// Light theme colors (GitHub-inspired)
const lightColors = {
    coral: '#cf222e',
    cyan: '#0969da',
    ivory: '#24292f',
    stone: '#6e7781',
    malibu: '#0550ae',
    whiskey: '#953800',
    violet: '#8250df',
    lightBackground: '#ffffff',
    highlightBackground: '#f6f8fa',
    background: '#ffffff',
    tooltipBackground: '#f6f8fa',
    selection: '#b6e3ff',
    cursor: '#24292f'
};

/// Dark theme for Antigravity
export const antigravityDarkTheme = EditorView.theme(
    {
        '&': {
            color: darkColors.ivory,
            backgroundColor: darkColors.background
        },

        '.cm-content': {
            caretColor: darkColors.cursor
        },

        '.cm-cursor, .cm-dropCursor': { borderLeftColor: darkColors.cursor },
        '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection':
            { backgroundColor: darkColors.selection },

        '.cm-panels': { backgroundColor: darkColors.darkBackground, color: darkColors.ivory },
        '.cm-panels.cm-panels-top': { borderBottom: '2px solid black' },
        '.cm-panels.cm-panels-bottom': { borderTop: '2px solid black' },

        '.cm-searchMatch': {
            backgroundColor: '#72a1ff59',
            outline: '1px solid #457dff'
        },
        '.cm-searchMatch.cm-searchMatch-selected': {
            backgroundColor: '#6199ff2f'
        },

        '.cm-activeLine': { backgroundColor: darkColors.highlightBackground },
        '.cm-selectionMatch': { backgroundColor: '#aafe661a' },

        '&.cm-focused .cm-matchingBracket, &.cm-focused .cm-nonmatchingBracket': {
            backgroundColor: '#bad0f847'
        },

        '.cm-gutters': {
            backgroundColor: darkColors.background,
            color: darkColors.stone,
            border: 'none'
        },

        '.cm-activeLineGutter': {
            backgroundColor: darkColors.highlightBackground
        },

        '.cm-foldPlaceholder': {
            backgroundColor: 'transparent',
            border: 'none',
            color: '#ddd'
        },

        '.cm-tooltip': {
            border: 'none',
            backgroundColor: darkColors.tooltipBackground
        },
        '.cm-tooltip .cm-tooltip-arrow:before': {
            borderTopColor: 'transparent',
            borderBottomColor: 'transparent'
        },
        '.cm-tooltip .cm-tooltip-arrow:after': {
            borderTopColor: darkColors.tooltipBackground,
            borderBottomColor: darkColors.tooltipBackground
        },
        '.cm-tooltip-autocomplete': {
            '& > ul > li[aria-selected]': {
                backgroundColor: darkColors.highlightBackground,
                color: darkColors.ivory
            }
        }
    },
    { dark: true }
);

/// Light theme for Antigravity
export const antigravityLightTheme = EditorView.theme(
    {
        '&': {
            color: lightColors.ivory,
            backgroundColor: lightColors.background
        },

        '.cm-content': {
            caretColor: lightColors.cursor
        },

        '.cm-cursor, .cm-dropCursor': { borderLeftColor: lightColors.cursor },
        '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection':
            { backgroundColor: lightColors.selection },

        '.cm-panels': { backgroundColor: lightColors.lightBackground, color: lightColors.ivory },
        '.cm-panels.cm-panels-top': { borderBottom: '2px solid #e1e4e8' },
        '.cm-panels.cm-panels-bottom': { borderTop: '2px solid #e1e4e8' },

        '.cm-searchMatch': {
            backgroundColor: '#fff8c5',
            outline: '1px solid #ffd33d'
        },
        '.cm-searchMatch.cm-searchMatch-selected': {
            backgroundColor: '#ffea7f'
        },

        '.cm-activeLine': { backgroundColor: lightColors.highlightBackground },
        '.cm-selectionMatch': { backgroundColor: '#c8e1ff' },

        '&.cm-focused .cm-matchingBracket, &.cm-focused .cm-nonmatchingBracket': {
            backgroundColor: '#c8e1ff'
        },

        '.cm-gutters': {
            backgroundColor: lightColors.background,
            color: lightColors.stone,
            border: 'none'
        },

        '.cm-activeLineGutter': {
            backgroundColor: lightColors.highlightBackground
        },

        '.cm-foldPlaceholder': {
            backgroundColor: 'transparent',
            border: 'none',
            color: '#999'
        },

        '.cm-tooltip': {
            border: '1px solid #e1e4e8',
            backgroundColor: lightColors.tooltipBackground
        },
        '.cm-tooltip .cm-tooltip-arrow:before': {
            borderTopColor: 'transparent',
            borderBottomColor: 'transparent'
        },
        '.cm-tooltip .cm-tooltip-arrow:after': {
            borderTopColor: lightColors.tooltipBackground,
            borderBottomColor: lightColors.tooltipBackground
        },
        '.cm-tooltip-autocomplete': {
            '& > ul > li[aria-selected]': {
                backgroundColor: lightColors.highlightBackground,
                color: lightColors.ivory
            }
        }
    },
    { dark: false }
);

/// Dark theme highlighting style
export const antigravityDarkHighlightStyle = HighlightStyle.define([
    { tag: t.keyword, color: darkColors.cyan },
    {
        tag: [t.name, t.deleted, t.character, t.propertyName, t.macroName],
        color: darkColors.coral
    },
    { tag: [t.function(t.variableName), t.labelName], color: darkColors.violet },
    { tag: [t.color, t.constant(t.name), t.standard(t.name)], color: darkColors.whiskey },
    { tag: [t.definition(t.name), t.separator], color: darkColors.ivory },
    {
        tag: [
            t.typeName,
            t.className,
            t.number,
            t.changed,
            t.annotation,
            t.modifier,
            t.self,
            t.namespace
        ],
        color: darkColors.whiskey
    },
    {
        tag: [
            t.operator,
            t.operatorKeyword,
            t.url,
            t.escape,
            t.regexp,
            t.link,
            t.special(t.string)
        ],
        color: darkColors.cyan
    },
    { tag: [t.meta, t.comment], color: darkColors.stone },
    { tag: t.strong, fontWeight: 'bold' },
    { tag: t.emphasis, fontStyle: 'italic' },
    { tag: t.strikethrough, textDecoration: 'line-through' },
    { tag: t.link, color: darkColors.stone, textDecoration: 'underline' },
    { tag: t.heading, fontWeight: 'bold', color: darkColors.coral },
    { tag: [t.atom, t.bool, t.special(t.variableName)], color: darkColors.whiskey },
    { tag: [t.processingInstruction, t.string, t.inserted], color: darkColors.malibu },
    { tag: t.invalid, color: darkColors.invalid }
]);

/// Light theme highlighting style
export const antigravityLightHighlightStyle = HighlightStyle.define([
    { tag: t.keyword, color: lightColors.cyan },
    {
        tag: [t.name, t.deleted, t.character, t.propertyName, t.macroName],
        color: lightColors.coral
    },
    { tag: [t.function(t.variableName), t.labelName], color: lightColors.violet },
    { tag: [t.color, t.constant(t.name), t.standard(t.name)], color: lightColors.whiskey },
    { tag: [t.definition(t.name), t.separator], color: lightColors.ivory },
    {
        tag: [
            t.typeName,
            t.className,
            t.number,
            t.changed,
            t.annotation,
            t.modifier,
            t.self,
            t.namespace
        ],
        color: lightColors.whiskey
    },
    {
        tag: [
            t.operator,
            t.operatorKeyword,
            t.url,
            t.escape,
            t.regexp,
            t.link,
            t.special(t.string)
        ],
        color: lightColors.cyan
    },
    { tag: [t.meta, t.comment], color: lightColors.stone },
    { tag: t.strong, fontWeight: 'bold' },
    { tag: t.emphasis, fontStyle: 'italic' },
    { tag: t.strikethrough, textDecoration: 'line-through' },
    { tag: t.link, color: lightColors.stone, textDecoration: 'underline' },
    { tag: t.heading, fontWeight: 'bold', color: lightColors.coral },
    { tag: [t.atom, t.bool, t.special(t.variableName)], color: lightColors.whiskey },
    { tag: [t.processingInstruction, t.string, t.inserted], color: lightColors.malibu },
    { tag: t.invalid, color: lightColors.coral }
]);

/// Extension to enable the Antigravity dark theme
export const antigravityDark: Extension = [
    antigravityDarkTheme,
    syntaxHighlighting(antigravityDarkHighlightStyle)
];

/// Extension to enable the Antigravity light theme
export const antigravityLight: Extension = [
    antigravityLightTheme,
    syntaxHighlighting(antigravityLightHighlightStyle)
];

// Default export for backward compatibility (dark theme)
export const antigravity = antigravityDark;

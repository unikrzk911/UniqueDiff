<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/uniquediff-logo-dark.svg">
    <img src="assets/uniquediff-logo-light.svg" alt="UniqueDiff" width="320">
  </picture>
</p>

<p align="center">
  Compare two blocks of text or code in your browser — side-by-side or unified, with syntax highlighting.
</p>

## Features

- **Paste or upload** text on each side; **Swap** and **Clear** in one click.
- **Two views:** side-by-side (both sides scroll together) or inline unified diff.
- **Granularity:** Line, Word, or Character highlighting within changed lines.
- **Ignore options:** whitespace, case, line endings (CRLF/LF), blank lines.
- **Syntax highlighting** for 19 languages, auto-detected from filename or content.
- **Overview ruler** marking every change; click a mark to jump to it.
- **Summary:** added / removed / changed line counts and similarity %.
- **Export:** `.diff`, standalone `.html` (with highlighting), or the original/changed `.txt`.
- **Private:** everything stays in memory for the session; nothing is saved or logged.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## How it works

| Option | What it does |
| --- | --- |
| Granularity | Lines are always aligned line-by-line. Word/Character mode only refines the highlight *inside* replaced lines. Summary counts are line-based. |
| Ignore options | Affect only the diff and its display. The Original/Changed downloads are always your exact input. |
| Syntax highlighting | Auto-detect tries the uploaded filename, then the content, and falls back to plain text. Pick a language or "None" to override. Both sides use the same language. |

## Project structure

```
app.py          Streamlit UI: inputs, options, toolbar, summary, diff view, export
diff_engine.py  difflib line alignment, word/char sub-diffs, stats, unified diff text
rendering.py    diff rows → HTML (side-by-side, inline, export), overview ruler
syntax.py       Pygments lexer detection, per-line tokenizing, span merging
utils.py        file decoding, text normalization, counts
styles.py       CSS: theme, diff colors, syntax token colors
assets/         logo and favicon (SVG)
tests/          unit tests for diff engine, rendering, syntax
```

## Tests

```bash
pip install pytest
pytest
```
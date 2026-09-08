# UniqueDiff

A Streamlit app for comparing two blocks of text — paste or upload, pick line/word/character
granularity, and see additions and removals highlighted side-by-side or as a unified diff.
Optional syntax highlighting colors the code by language on top of the diff highlighting.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

- `app.py` — Streamlit UI: inputs, options, toolbar, summary, diff view, export.
- `diff_engine.py` — line-alignment via `difflib.SequenceMatcher`, plus word/char inline
  sub-diffing for replaced lines, stats, and unified-diff text.
- `rendering.py` — turns diff rows into highlighted HTML (side-by-side and inline views),
  layering syntax colors from `syntax.py` under the diff highlighting when a language is set.
- `syntax.py` — Pygments-backed language detection (from an uploaded filename or content) and
  tokenization, plus the logic that merges token spans with diff spans for rendering.
- `utils.py` — file decoding, text normalization (whitespace/case/line-ending/blank-line
  options), character/word/line counts.
- `styles.py` — CSS for the highlight colors, layout, and syntax token colors.
- `tests/test_diff_engine.py`, `tests/test_rendering.py`, `tests/test_syntax.py` — unit tests
  for the diff/normalize/stats logic, HTML rendering, and syntax highlighting.

## Notes

- All processing is in-memory for the session; nothing is written to disk or logged.
- Diff granularity (Line/Word/Character) controls how *replaced* lines are sub-highlighted —
  line mode highlights the whole line, word/character mode highlight just the changed range
  within it. Line alignment itself (which lines correspond to which) is always computed at
  the line level, which is also what the summary counts (added/removed/changed) are based on.
- "Ignore whitespace/case/line-endings/blank lines" only affect the diff computation and
  display — the Original/Changed downloads always contain your exact, unmodified input.
- Syntax highlighting (sidebar) defaults to Auto-detect — it guesses from an uploaded file's
  extension first, then from content, and falls back to no coloring if neither is confident.
  Pick a language explicitly, or "None", to override. The same language is used for both
  sides so the two panes stay visually consistent, and highlighting is included in the
  `.html` export as well as the on-screen views.

## Author

**Unique Rajak**
- LinkedIn: https://www.linkedin.com/in/unikrzk/
- Email: unique.rajak.p@gmail.com

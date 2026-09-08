# UniqueDiff

A Streamlit app for comparing two blocks of text — paste or upload, pick line/word/character
granularity, and see additions and removals highlighted side-by-side or as a unified diff.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

- `app.py` — Streamlit UI: inputs, options, toolbar, summary, diff view, export.
- `diff_engine.py` — line-alignment via `difflib.SequenceMatcher`, plus word/char inline
  sub-diffing for replaced lines, stats, and unified-diff text.
- `rendering.py` — turns diff rows into highlighted HTML (side-by-side and inline views).
- `utils.py` — file decoding, text normalization (whitespace/case/line-ending/blank-line
  options), character/word/line counts.
- `styles.py` — CSS for the highlight colors and layout.
- `tests/test_diff_engine.py` — unit tests for the diff/normalize/stats logic.

## Notes

- All processing is in-memory for the session; nothing is written to disk or logged.
- Diff granularity (Line/Word/Character) controls how *replaced* lines are sub-highlighted —
  line mode highlights the whole line, word/character mode highlight just the changed range
  within it. Line alignment itself (which lines correspond to which) is always computed at
  the line level, which is also what the summary counts (added/removed/changed) are based on.
- "Ignore whitespace/case/line-endings/blank lines" only affect the diff computation and
  display — the Original/Changed downloads always contain your exact, unmodified input.

## Author

**Unique Rajak**
- LinkedIn: https://www.linkedin.com/in/unikrzk/
- Email: unique.rajak.p@gmail.com

import html


def _spans_to_html(spans):
    if not spans:
        return '<span class="diff-blank">&nbsp;</span>'
    out = []
    for tag, text in spans:
        escaped = html.escape(text) or '&nbsp;'
        css_class = {'equal': 'diff-equal', 'delete': 'diff-del', 'insert': 'diff-add'}[tag]
        out.append(f'<span class="{css_class}">{escaped}</span>')
    return ''.join(out)


def render_side_by_side(rows):
    """Returns (left_html, right_html) for the two side-by-side panes."""
    left_rows, right_rows = [], []
    for row in rows:
        row_class = f"row-{row['tag']}"
        a_no = row['a_no'] if row['a_no'] else ''
        b_no = row['b_no'] if row['b_no'] else ''
        left_rows.append(
            f'<div class="diff-row {row_class}"><span class="line-no">{a_no}</span>'
            f'<span class="line-content">{_spans_to_html(row["a_spans"])}</span></div>'
        )
        right_rows.append(
            f'<div class="diff-row {row_class}"><span class="line-no">{b_no}</span>'
            f'<span class="line-content">{_spans_to_html(row["b_spans"])}</span></div>'
        )
    return (
        f'<div class="diff-pane">{"".join(left_rows)}</div>',
        f'<div class="diff-pane">{"".join(right_rows)}</div>',
    )


def render_inline(rows):
    """Single-column unified-style view: equal lines plain, replaced/deleted/inserted with +/- markers."""
    parts = []
    for row in rows:
        if row['tag'] == 'equal':
            parts.append(
                '<div class="diff-row row-equal"><span class="marker">&nbsp;</span>'
                f'<span class="line-content">{_spans_to_html(row["a_spans"])}</span></div>'
            )
            continue
        if row['a_spans']:
            parts.append(
                '<div class="diff-row row-delete"><span class="marker">-</span>'
                f'<span class="line-content">{_spans_to_html(row["a_spans"])}</span></div>'
            )
        if row['b_spans']:
            parts.append(
                '<div class="diff-row row-insert"><span class="marker">+</span>'
                f'<span class="line-content">{_spans_to_html(row["b_spans"])}</span></div>'
            )
    return f'<div class="diff-pane">{"".join(parts)}</div>'


def render_full_html_export(rows, css):
    left_html, right_html = render_side_by_side(rows)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Diff Result</title>
<style>{css}</style>
</head>
<body>
<div class="diff-container">
  <div class="diff-column"><h3>Original</h3>{left_html}</div>
  <div class="diff-column"><h3>Changed</h3>{right_html}</div>
</div>
</body>
</html>"""

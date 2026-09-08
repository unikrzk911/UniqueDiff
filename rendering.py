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


def _row_div(row_class, gutter_class, gutter_content, spans):
    return (
        f'<div class="diff-row {row_class}"><span class="{gutter_class}">{gutter_content}</span>'
        f'<span class="line-content">{_spans_to_html(spans)}</span></div>'
    )


def render_side_by_side(rows):
    """Returns (left_html, right_html) for the two side-by-side panes."""
    left_rows, right_rows = [], []
    for row in rows:
        row_class = f"row-{row['tag']}"
        left_rows.append(_row_div(row_class, 'line-no', row['a_no'] or '', row['a_spans']))
        right_rows.append(_row_div(row_class, 'line-no', row['b_no'] or '', row['b_spans']))
    return (
        f'<div class="diff-pane">{"".join(left_rows)}</div>',
        f'<div class="diff-pane">{"".join(right_rows)}</div>',
    )


def render_inline(rows):
    """Single-column unified-style view: equal lines plain, replaced/deleted/inserted with +/- markers."""
    parts = []
    for row in rows:
        if row['tag'] == 'equal':
            parts.append(_row_div('row-equal', 'marker', '&nbsp;', row['a_spans']))
            continue
        if row['a_spans']:
            parts.append(_row_div('row-delete', 'marker', '-', row['a_spans']))
        if row['b_spans']:
            parts.append(_row_div('row-insert', 'marker', '+', row['b_spans']))
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

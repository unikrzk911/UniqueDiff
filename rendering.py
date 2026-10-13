import html

import syntax


def _spans_to_html(spans, token_spans=None):
    if not spans:
        return '<span class="diff-blank">&nbsp;</span>'
    if token_spans:
        pieces = [
            (tag, syntax.token_css_class(ttype) if ttype is not None else '', text)
            for tag, ttype, text in syntax.merge_spans(spans, token_spans)
        ]
    else:
        pieces = [(tag, '', text) for tag, text in spans]
    out = []
    for tag, hl_class, text in pieces:
        escaped = html.escape(text) or '&nbsp;'
        diff_class = {'equal': 'diff-equal', 'delete': 'diff-del', 'insert': 'diff-add'}[tag]
        classes = f"{diff_class} hl-{hl_class}" if hl_class else diff_class
        out.append(f'<span class="{classes}">{escaped}</span>')
    return ''.join(out)


def _row_div(row_class, gutter_class, gutter_content, spans, token_spans=None):
    return (
        f'<div class="diff-row {row_class}"><span class="{gutter_class}">{gutter_content}</span>'
        f'<span class="line-content">{_spans_to_html(spans, token_spans)}</span></div>'
    )


def _pane(row_divs, tags, pane_id):
    """Wraps rendered rows in a scrollable pane plus a VS Code-style overview ruler.

    tags[i] is the diff tag of row_divs[i]; each run of non-equal rows becomes one
    ruler mark, placed proportionally and linking to the run's first row.
    """
    total = len(tags) or 1
    marks, rows = [], list(row_divs)
    i = 0
    while i < len(tags):
        j = i
        while j < len(tags) and tags[j] == tags[i]:
            j += 1
        if tags[i] != 'equal':
            anchor = f'{pane_id}-{i}'
            rows[i] = rows[i].replace('<div ', f'<div id="{anchor}" ', 1)
            marks.append(
                f'<a class="ruler-mark ruler-{tags[i]}" href="#{anchor}" '
                f'style="top:{i / total * 100:.3f}%;height:{(j - i) / total * 100:.3f}%"></a>'
            )
        i = j
    return (
        f'<div class="diff-wrap"><div class="diff-pane">{"".join(rows)}</div>'
        f'<div class="diff-ruler">{"".join(marks)}</div></div>'
    )


def _line_tokens(tokens, line_no):
    """tokens is a per-line token list (see syntax.tokenize_text_by_line); line_no is 1-based or None."""
    return tokens[line_no - 1] if tokens and line_no else None


def render_side_by_side(rows, tokens_a=None, tokens_b=None):
    """Returns one pane where each row pairs the original and changed line, so both
    sides scroll together and wrapped lines stay aligned.

    tokens_a/tokens_b are optional per-line Pygments token lists that layer
    syntax colors under the diff highlighting; omit for plain rendering.
    """
    pairs = []
    for row in rows:
        row_class = f"row-{row['tag']}"
        left = _row_div(row_class, 'line-no', row['a_no'] or '', row['a_spans'], _line_tokens(tokens_a, row['a_no']))
        right = _row_div(row_class, 'line-no', row['b_no'] or '', row['b_spans'], _line_tokens(tokens_b, row['b_no']))
        pairs.append(f'<div class="diff-pair">{left}{right}</div>')
    return _pane(pairs, [row['tag'] for row in rows], 's')


def render_inline(rows, tokens_a=None, tokens_b=None):
    """Single-column unified-style view: equal lines plain, replaced/deleted/inserted with +/- markers."""
    parts, tags = [], []
    for row in rows:
        if row['tag'] == 'equal':
            parts.append(_row_div('row-equal', 'marker', '&nbsp;', row['a_spans'], _line_tokens(tokens_a, row['a_no'])))
            tags.append('equal')
            continue
        if row['a_spans']:
            parts.append(_row_div('row-delete', 'marker', '-', row['a_spans'], _line_tokens(tokens_a, row['a_no'])))
            tags.append('delete')
        if row['b_spans']:
            parts.append(_row_div('row-insert', 'marker', '+', row['b_spans'], _line_tokens(tokens_b, row['b_no'])))
            tags.append('insert')
    return _pane(parts, tags, 'u')


def render_full_html_export(rows, css, tokens_a=None, tokens_b=None):
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Diff Result</title>
<style>{css}</style>
</head>
<body>
<div class="diff-pair"><h3>Original</h3><h3>Changed</h3></div>
{render_side_by_side(rows, tokens_a, tokens_b)}
</body>
</html>"""

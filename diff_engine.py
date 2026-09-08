import difflib
import re

_WORD_TOKEN_RE = re.compile(r'[^\S\r\n]+|\w+|[^\w\s]')


def _tokenize_words(text):
    return _WORD_TOKEN_RE.findall(text)


def _tokenize_chars(text):
    return list(text)


def _inline_diff(line_a, line_b, granularity):
    """Sub-line diff for a pair of replaced lines. granularity: 'word' or 'char'."""
    if granularity == 'char':
        tokens_a, tokens_b = _tokenize_chars(line_a), _tokenize_chars(line_b)
    else:
        tokens_a, tokens_b = _tokenize_words(line_a), _tokenize_words(line_b)
    sm = difflib.SequenceMatcher(None, tokens_a, tokens_b, autojunk=False)
    return [
        (tag, ''.join(tokens_a[i1:i2]), ''.join(tokens_b[j1:j2]))
        for tag, i1, i2, j1, j2 in sm.get_opcodes()
    ]


def _row(tag, a_no, a_spans, b_no, b_spans):
    return {'tag': tag, 'a_no': a_no, 'b_no': b_no, 'a_spans': a_spans, 'b_spans': b_spans}


def _equal_rows(lines_a, lines_b, i1, i2, j1, j2):
    return [
        _row('equal', a_idx + 1, [('equal', lines_a[a_idx])], b_idx + 1, [('equal', lines_b[b_idx])])
        for a_idx, b_idx in zip(range(i1, i2), range(j1, j2))
    ]


def _delete_rows(lines_a, i1, i2):
    return [_row('delete', a_idx + 1, [('delete', lines_a[a_idx])], None, []) for a_idx in range(i1, i2)]


def _insert_rows(lines_b, j1, j2):
    return [_row('insert', None, [], b_idx + 1, [('insert', lines_b[b_idx])]) for b_idx in range(j1, j2)]


def _replace_spans(line_a, line_b, granularity):
    """Sub-spans for one paired replaced line, per the requested granularity."""
    if granularity == 'line':
        return [('delete', line_a)], [('insert', line_b)]
    a_spans, b_spans = [], []
    for op_tag, a_txt, b_txt in _inline_diff(line_a, line_b, granularity):
        if op_tag == 'equal':
            a_spans.append(('equal', a_txt))
            b_spans.append(('equal', b_txt))
        elif op_tag == 'delete':
            a_spans.append(('delete', a_txt))
        elif op_tag == 'insert':
            b_spans.append(('insert', b_txt))
        elif op_tag == 'replace':
            a_spans.append(('delete', a_txt))
            b_spans.append(('insert', b_txt))
    return a_spans, b_spans


def _replace_rows(lines_a, lines_b, i1, i2, j1, j2, granularity):
    paired = min(i2 - i1, j2 - j1)
    rows = []
    for offset in range(paired):
        a_idx, b_idx = i1 + offset, j1 + offset
        a_spans, b_spans = _replace_spans(lines_a[a_idx], lines_b[b_idx], granularity)
        rows.append(_row('replace', a_idx + 1, a_spans, b_idx + 1, b_spans))
    rows += _delete_rows(lines_a, i1 + paired, i2)
    rows += _insert_rows(lines_b, j1 + paired, j2)
    return rows


def compute_line_diff(text_a, text_b, granularity='line'):
    """
    Line-aligns text_a/text_b with difflib and returns a list of row dicts:
    {tag, a_no, b_no, a_spans, b_spans} where spans are [(tag, text), ...].

    granularity ('line' | 'word' | 'char') controls whether replaced line
    pairs get inline sub-highlighting, and at what resolution.
    """
    lines_a = text_a.splitlines()
    lines_b = text_b.splitlines()
    sm = difflib.SequenceMatcher(None, lines_a, lines_b, autojunk=False)
    rows = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            rows += _equal_rows(lines_a, lines_b, i1, i2, j1, j2)
        elif tag == 'delete':
            rows += _delete_rows(lines_a, i1, i2)
        elif tag == 'insert':
            rows += _insert_rows(lines_b, j1, j2)
        elif tag == 'replace':
            rows += _replace_rows(lines_a, lines_b, i1, i2, j1, j2, granularity)
    return rows


def compute_stats(text_a, text_b):
    """Line-level added/removed/changed counts plus overall similarity %."""
    lines_a, lines_b = text_a.splitlines(), text_b.splitlines()
    sm = difflib.SequenceMatcher(None, lines_a, lines_b, autojunk=False)
    added = removed = changed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'insert':
            added += j2 - j1
        elif tag == 'delete':
            removed += i2 - i1
        elif tag == 'replace':
            a_n, b_n = i2 - i1, j2 - j1
            changed += min(a_n, b_n)
            added += max(0, b_n - a_n)
            removed += max(0, a_n - b_n)
    return {
        'added': added,
        'removed': removed,
        'changed': changed,
        'similarity': round(sm.ratio() * 100, 1),
    }


def unified_diff_text(text_a, text_b, label_a='Original', label_b='Changed'):
    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)
    diff = difflib.unified_diff(lines_a, lines_b, fromfile=label_a, tofile=label_b, lineterm='')
    return '\n'.join(diff)

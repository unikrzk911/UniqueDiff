"""Pygments-backed syntax highlighting for the diff view.

Tokenizes whole texts (not line-by-line) so multi-line constructs like
triple-quoted strings and block comments keep correct lexer state, then
splits the resulting token stream into per-line lists that line up with
diff_engine's line numbering. merge_spans() refines a line's diff spans
(equal/delete/insert) against its token spans so both can be rendered
as nested HTML without diff_engine or rendering knowing about Pygments.
"""
from pygments.lexers import get_lexer_by_name, guess_lexer, guess_lexer_for_filename
from pygments.token import STANDARD_TYPES
from pygments.util import ClassNotFound

LANGUAGE_CHOICES = {
    "Auto-detect": "auto",
    "None (plain text)": None,
    "Python": "python",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "JSON": "json",
    "YAML": "yaml",
    "HTML": "html",
    "CSS": "css",
    "SQL": "sql",
    "Java": "java",
    "C": "c",
    "C++": "cpp",
    "C#": "csharp",
    "Go": "go",
    "Rust": "rust",
    "Shell": "bash",
    "Markdown": "markdown",
    "XML": "xml",
    "PHP": "php",
    "Ruby": "ruby",
}

_LEXER_OPTIONS = {"stripnl": False, "stripall": False}


def resolve_lexer(choice_label, text_a, text_b, filename_a=None, filename_b=None):
    """Pick one lexer to use for both sides of the diff, or None for plain text.

    'Auto-detect' tries the uploaded filenames first (deterministic), then
    falls back to guessing from content. Returns None if nothing is
    confident enough, so callers can degrade to plain rendering.
    """
    alias = LANGUAGE_CHOICES.get(choice_label, "auto")
    if alias is None:
        return None
    if alias != "auto":
        return get_lexer_by_name(alias, **_LEXER_OPTIONS)

    for filename, text in ((filename_a, text_a), (filename_b, text_b)):
        if filename:
            try:
                return guess_lexer_for_filename(filename, text or " ", **_LEXER_OPTIONS)
            except ClassNotFound:
                continue
    for text in (text_a, text_b):
        if text and text.strip():
            try:
                return guess_lexer(text, **_LEXER_OPTIONS)
            except ClassNotFound:
                continue
    return None


def tokenize_text_by_line(text, lexer):
    """Lex the whole text once, then split into one token list per line.

    A token's text can span a newline (e.g. a multi-line string), so
    tokens are cut at each '\\n' and distributed to the line they belong to.
    """
    line_count = len(text.splitlines())
    if line_count == 0:
        return []
    lines = [[] for _ in range(line_count)]
    line_idx = 0
    for ttype, ttext in lexer.get_tokens(text):
        while ttext:
            nl_pos = ttext.find('\n')
            if nl_pos == -1:
                if line_idx < line_count:
                    lines[line_idx].append((ttype, ttext))
                break
            segment = ttext[:nl_pos]
            if segment and line_idx < line_count:
                lines[line_idx].append((ttype, segment))
            ttext = ttext[nl_pos + 1:]
            line_idx += 1
    return lines


def merge_spans(diff_spans, token_spans):
    """Refine diff_spans [(diff_tag, text)] against token_spans [(ttype, text)]
    covering the same line, yielding [(diff_tag, ttype, text)] pieces that
    respect both sets of boundaries.
    """
    if not token_spans:
        return [(tag, None, text) for tag, text in diff_spans]
    pieces = []
    ti, toff = 0, 0
    for dtag, dtext in diff_spans:
        if dtext == '':
            pieces.append((dtag, None, ''))
            continue
        doff = 0
        while doff < len(dtext):
            ttype, ttext = token_spans[ti]
            take = min(len(dtext) - doff, len(ttext) - toff)
            pieces.append((dtag, ttype, dtext[doff:doff + take]))
            doff += take
            toff += take
            if toff == len(ttext):
                ti += 1
                toff = 0
    return pieces


def token_css_class(ttype):
    """Short Pygments class code (e.g. 'kr' for Keyword.Reserved) for a token type."""
    while ttype not in STANDARD_TYPES:
        ttype = ttype.parent
    return STANDARD_TYPES[ttype]

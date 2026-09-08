import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.token import Keyword, Token

import syntax


def test_resolve_lexer_none_choice_returns_none():
    assert syntax.resolve_lexer("None (plain text)", "a", "b") is None


def test_resolve_lexer_explicit_choice():
    lexer = syntax.resolve_lexer("Python", "a", "b")
    assert isinstance(lexer, PythonLexer)


def test_resolve_lexer_auto_detects_from_filename():
    lexer = syntax.resolve_lexer("Auto-detect", "print(1)", "print(2)", filename_a="a.py")
    assert isinstance(lexer, PythonLexer)


def test_resolve_lexer_auto_is_harmless_for_ambiguous_text():
    # Pygments' guess_lexer() falls back to TextLexer for prose rather than
    # raising, so assert the practical effect: no coloring is produced.
    lexer = syntax.resolve_lexer("Auto-detect", "hello world", "hello there")
    if lexer is None:
        return
    lines = syntax.tokenize_text_by_line("hello world", lexer)
    classes = {syntax.token_css_class(ttype) for line in lines for ttype, _ in line}
    assert classes <= {''}


def test_tokenize_text_by_line_preserves_leading_blank_lines():
    lexer = get_lexer_by_name("python")
    text = "\n\ndef f():\n    pass\n"
    lines = syntax.tokenize_text_by_line(text, lexer)
    assert len(lines) == len(text.splitlines())


def test_tokenize_text_by_line_empty_text():
    lexer = get_lexer_by_name("python")
    assert syntax.tokenize_text_by_line("", lexer) == []


def test_tokenize_text_by_line_reconstructs_each_line():
    lexer = get_lexer_by_name("python")
    text = "def f():\n    return 'a\\nb'\n"
    lines = syntax.tokenize_text_by_line(text, lexer)
    original_lines = text.splitlines()
    assert len(lines) == len(original_lines)
    for line_tokens, original in zip(lines, original_lines):
        assert ''.join(t for _, t in line_tokens) == original


def test_tokenize_text_by_line_handles_multiline_token():
    lexer = get_lexer_by_name("python")
    text = 'x = """\nline two\n"""\n'
    lines = syntax.tokenize_text_by_line(text, lexer)
    original_lines = text.splitlines()
    assert len(lines) == len(original_lines)
    assert ''.join(t for _, t in lines[1]) == "line two"


def test_tokenize_text_by_line_finds_keyword():
    lexer = get_lexer_by_name("python")
    lines = syntax.tokenize_text_by_line("def f():\n    pass\n", lexer)
    assert any(ttype in Keyword for ttype, _ in lines[0])


def test_merge_spans_no_token_spans_passes_through():
    result = syntax.merge_spans([('equal', 'abcd')], None)
    assert result == [('equal', None, 'abcd')]


def test_merge_spans_splits_at_both_boundaries():
    diff_spans = [('equal', 'ab'), ('delete', 'cd')]
    token_spans = [('TokA', 'a'), ('TokB', 'bcd')]
    result = syntax.merge_spans(diff_spans, token_spans)
    assert result == [
        ('equal', 'TokA', 'a'),
        ('equal', 'TokB', 'b'),
        ('delete', 'TokB', 'cd'),
    ]
    assert ''.join(piece[2] for piece in result) == 'abcd'


def test_merge_spans_empty_span_preserved():
    result = syntax.merge_spans([('equal', '')], [])
    assert result == [('equal', None, '')]


def test_merge_spans_empty_diff_spans_list():
    assert syntax.merge_spans([], [('TokA', 'x')]) == []


def test_token_css_class_direct_hit():
    assert syntax.token_css_class(Keyword) == 'k'


def test_token_css_class_root_is_empty_string():
    assert syntax.token_css_class(Token) == ''


def test_token_css_class_falls_back_to_nearest_standard_ancestor():
    from pygments.token import STANDARD_TYPES
    custom = Keyword.Reserved.Foo
    assert syntax.token_css_class(custom) == STANDARD_TYPES[Keyword.Reserved]

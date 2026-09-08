import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pygments.lexers import get_lexer_by_name

import diff_engine
import rendering
import syntax


def test_render_side_by_side_unchanged_without_tokens():
    rows = diff_engine.compute_line_diff("def f():\n    pass", "def f():\n    pass")
    with_tokens = rendering.render_side_by_side(rows)
    without_tokens = rendering.render_side_by_side(rows, tokens_a=None, tokens_b=None)
    assert with_tokens == without_tokens
    assert 'hl-' not in with_tokens[0]


def test_render_side_by_side_adds_token_classes():
    text = "def f():\n    pass\n"
    rows = diff_engine.compute_line_diff(text, text)
    lexer = get_lexer_by_name("python")
    tokens = syntax.tokenize_text_by_line(text, lexer)
    left_html, right_html = rendering.render_side_by_side(rows, tokens_a=tokens, tokens_b=tokens)
    assert 'hl-k' in left_html  # 'def' is a keyword
    assert 'hl-k' in right_html


def test_render_inline_adds_token_classes_for_insert_and_delete():
    text_a = "old = 1\n"
    text_b = "new = 2\n"
    rows = diff_engine.compute_line_diff(text_a, text_b, granularity='line')
    lexer = get_lexer_by_name("python")
    tokens_a = syntax.tokenize_text_by_line(text_a, lexer)
    tokens_b = syntax.tokenize_text_by_line(text_b, lexer)
    html_out = rendering.render_inline(rows, tokens_a=tokens_a, tokens_b=tokens_b)
    assert 'hl-mi' in html_out  # integer literals 1 and 2


def test_render_full_html_export_includes_token_classes():
    text = "x = 1\n"
    rows = diff_engine.compute_line_diff(text, text)
    lexer = get_lexer_by_name("python")
    tokens = syntax.tokenize_text_by_line(text, lexer)
    export = rendering.render_full_html_export(rows, "", tokens_a=tokens, tokens_b=tokens)
    assert 'hl-mi' in export

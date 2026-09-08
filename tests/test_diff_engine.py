import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import diff_engine
import utils


def test_identical_text_has_no_diff_rows_but_all_equal():
    rows = diff_engine.compute_line_diff("a\nb\nc", "a\nb\nc")
    assert all(row["tag"] == "equal" for row in rows)
    assert len(rows) == 3


def test_pure_insert_and_delete():
    rows = diff_engine.compute_line_diff("a\nb", "a\nb\nc")
    tags = [row["tag"] for row in rows]
    assert tags == ["equal", "equal", "insert"]


def test_replace_line_mode_has_no_inline_spans():
    rows = diff_engine.compute_line_diff("hello world", "hello there", granularity="line")
    assert rows[0]["tag"] == "replace"
    assert rows[0]["a_spans"] == [("delete", "hello world")]
    assert rows[0]["b_spans"] == [("insert", "hello there")]


def test_replace_word_mode_highlights_only_changed_word():
    rows = diff_engine.compute_line_diff("hello world", "hello there", granularity="word")
    a_spans, b_spans = rows[0]["a_spans"], rows[0]["b_spans"]
    assert ("equal", "hello ") in a_spans
    assert ("delete", "world") in a_spans
    assert ("insert", "there") in b_spans


def test_compute_stats_counts_added_removed_changed():
    stats = diff_engine.compute_stats("a\nb\nc", "a\nx\nc\nd")
    assert stats["changed"] == 1
    assert stats["added"] == 1
    assert stats["removed"] == 0
    assert 0 <= stats["similarity"] <= 100


def test_unified_diff_text_contains_markers():
    diff_text = diff_engine.unified_diff_text("a\nb\n", "a\nc\n")
    assert "-b" in diff_text
    assert "+c" in diff_text


def test_normalize_ignore_case_and_whitespace():
    normalized = utils.normalize_text("Hello   World", ignore_whitespace=True, ignore_case=True)
    assert normalized == "hello world"


def test_normalize_ignore_blank_lines():
    normalized = utils.normalize_text("a\n\nb\n\n\nc", ignore_blank_lines=True)
    assert normalized == "a\nb\nc"


def test_count_stats():
    stats = utils.count_stats("hello world\nsecond line")
    assert stats["chars"] == len("hello world\nsecond line")
    assert stats["words"] == 4
    assert stats["lines"] == 2

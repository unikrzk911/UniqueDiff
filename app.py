import html as html_lib

import streamlit as st

import diff_engine
import rendering
import utils
from styles import DIFF_CSS

MAX_RECOMMENDED_CHARS = 200_000
MODE_MAP = {"Line": "line", "Word": "word", "Character": "char"}

st.set_page_config(page_title="Diff Checker", page_icon="🔍", layout="wide")
st.markdown(f"<style>{DIFF_CSS}</style>", unsafe_allow_html=True)

st.title("🔍 Diff Checker")
st.caption("Paste or upload two blocks of text to see what changed. Nothing is saved to disk.")

with st.sidebar:
    st.header("Options")
    mode_label = st.radio(
        "Diff granularity", list(MODE_MAP.keys()), index=0,
        help="Controls how differences within a changed line are highlighted.",
    )
    view = st.radio("View", ["Side-by-side", "Inline (unified)"], index=0)
    st.divider()
    ignore_whitespace = st.checkbox("Ignore whitespace")
    ignore_case = st.checkbox("Ignore case")
    ignore_line_endings = st.checkbox("Ignore line endings (CRLF/LF)")
    ignore_blank_lines = st.checkbox("Ignore blank lines")

mode_key = MODE_MAP[mode_label]

for key in ("text_a", "text_b"):
    if key not in st.session_state:
        st.session_state[key] = ""
if "has_compared" not in st.session_state:
    st.session_state.has_compared = False

tb1, tb2, tb3, _ = st.columns([1, 1, 1, 5])
with tb1:
    compare_clicked = st.button("Compare", type="primary", use_container_width=True)
with tb2:
    if st.button("Swap", use_container_width=True):
        st.session_state.text_a, st.session_state.text_b = st.session_state.text_b, st.session_state.text_a
with tb3:
    if st.button("Clear", use_container_width=True):
        st.session_state.text_a = ""
        st.session_state.text_b = ""
        st.session_state.has_compared = False

if compare_clicked:
    st.session_state.has_compared = True


def _panel(col, label, text_key, uploader_key, tracker_key):
    with col:
        st.subheader(label)
        uploaded = st.file_uploader(f"Upload for {label}", key=uploader_key, label_visibility="collapsed")
        if uploaded is not None:
            fingerprint = (uploaded.name, uploaded.size)
            if st.session_state.get(tracker_key) != fingerprint:
                st.session_state[text_key] = utils.read_uploaded_file(uploaded)
                st.session_state[tracker_key] = fingerprint
        st.text_area(
            label, key=text_key, height=300, label_visibility="collapsed",
            placeholder=f"Paste your {label.lower()} text here…",
        )
        stats = utils.count_stats(st.session_state[text_key])
        st.caption(f"{stats['chars']:,} chars · {stats['words']:,} words · {stats['lines']:,} lines")


col_a, col_b = st.columns(2)
_panel(col_a, "Original", "text_a", "uploader_a", "upload_fp_a")
_panel(col_b, "Changed", "text_b", "uploader_b", "upload_fp_b")

st.divider()

if not st.session_state.has_compared:
    st.info("Enter or upload text on both sides, then click **Compare**.")
    st.stop()

text_a_raw = st.session_state.text_a
text_b_raw = st.session_state.text_b

if not text_a_raw and not text_b_raw:
    st.warning("Both inputs are empty — nothing to compare.")
    st.stop()

for label, txt in (("Original", text_a_raw), ("Changed", text_b_raw)):
    if len(txt) > MAX_RECOMMENDED_CHARS:
        st.warning(f"{label} text is very large ({len(txt):,} characters) — the diff may take a moment.")

text_a = utils.normalize_text(text_a_raw, ignore_whitespace, ignore_case, ignore_line_endings, ignore_blank_lines)
text_b = utils.normalize_text(text_b_raw, ignore_whitespace, ignore_case, ignore_line_endings, ignore_blank_lines)

if text_a == text_b:
    st.success("No differences found — the two texts are identical (with the selected options applied).")
    st.stop()

rows = diff_engine.compute_line_diff(text_a, text_b, granularity=mode_key)
stats = diff_engine.compute_stats(text_a, text_b)

s1, s2, s3, s4 = st.columns(4)
s1.metric("Lines added", stats["added"])
s2.metric("Lines removed", stats["removed"])
s3.metric("Lines changed", stats["changed"])
s4.metric("Similarity", f"{stats['similarity']}%")

with st.expander("Legend"):
    st.markdown(
        '<span class="diff-add">&nbsp;Added&nbsp;</span>&nbsp;&nbsp;'
        '<span class="diff-del">&nbsp;Removed&nbsp;</span>&nbsp;&nbsp;'
        '<span class="diff-equal">Unchanged</span>',
        unsafe_allow_html=True,
    )

if view == "Side-by-side":
    left_html, right_html = rendering.render_side_by_side(rows)
    dcol_a, dcol_b = st.columns(2)
    with dcol_a:
        st.markdown("**Original**")
        st.markdown(left_html, unsafe_allow_html=True)
    with dcol_b:
        st.markdown("**Changed**")
        st.markdown(right_html, unsafe_allow_html=True)
else:
    st.markdown(rendering.render_inline(rows), unsafe_allow_html=True)

st.divider()
st.subheader("Export")

unified_text = diff_engine.unified_diff_text(text_a_raw, text_b_raw) or "No differences."
full_html_export = rendering.render_full_html_export(rows, DIFF_CSS)

e1, e2, e3, e4 = st.columns(4)
with e1:
    st.download_button("Diff (.diff)", unified_text, file_name="diff.diff", use_container_width=True)
with e2:
    st.download_button("Diff (.html)", full_html_export, file_name="diff.html", mime="text/html", use_container_width=True)
with e3:
    st.download_button("Original (.txt)", text_a_raw, file_name="original.txt", use_container_width=True)
with e4:
    st.download_button("Changed (.txt)", text_b_raw, file_name="changed.txt", use_container_width=True)

copy_widget = f"""
<textarea id="diff-copy-src" style="display:none">{html_lib.escape(unified_text)}</textarea>
<button onclick="navigator.clipboard.writeText(document.getElementById('diff-copy-src').value)"
        style="padding:6px 14px;border-radius:6px;border:1px solid #999;cursor:pointer;background:transparent;">
  Copy diff to clipboard
</button>
"""
st.iframe(copy_widget, height=45)

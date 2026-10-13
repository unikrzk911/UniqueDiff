# Brand colors from assets/uniquediff-logo.svg. light-dark() resolves where the variable is used,
# so inside the app it follows Streamlit's theme color-scheme; the HTML export falls back to light.
DIFF_CSS = """
:root {
  --ud-red: light-dark(#F2545B, #FF6B6B);
  --ud-green: light-dark(#12B886, #2DD4A7);
  --ud-line: light-dark(rgba(29, 29, 31, 0.10), rgba(245, 245, 247, 0.10));
}
.diff-pair { display: grid; grid-template-columns: 1fr 1fr; column-gap: 12px; }
.diff-pair > * { min-width: 0; }
.diff-wrap { display: flex; gap: 4px; }
.diff-wrap > .diff-pane { flex: 1; min-width: 0; }
.diff-ruler {
  position: relative;
  flex: 0 0 10px;
  border-radius: 5px;
  background: var(--ud-line);
  overflow: hidden;
}
.ruler-mark { position: absolute; left: 0; right: 0; min-height: 3px; transition: filter 120ms ease-out; }
.ruler-mark:hover { filter: brightness(1.25) saturate(1.2); }
.ruler-insert { background: var(--ud-green); }
.ruler-delete { background: var(--ud-red); }
.ruler-replace { background: linear-gradient(var(--ud-red), var(--ud-green)); }
.diff-pane {
  font-family: ui-monospace, 'SF Mono', 'SFMono-Regular', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.85rem;
  border: 1px solid var(--ud-line);
  border-radius: 12px;
  overflow: auto;
  max-height: 600px;
  scroll-behavior: smooth;
}
.diff-row {
  display: flex;
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1px 8px;
  line-height: 1.5;
}
.diff-row.row-delete { background: color-mix(in srgb, var(--ud-red) 12%, transparent); }
.diff-row.row-insert { background: color-mix(in srgb, var(--ud-green) 12%, transparent); }
.diff-row.row-replace { background: color-mix(in srgb, var(--ud-red) 5%, color-mix(in srgb, var(--ud-green) 5%, transparent)); }
.line-no {
  flex: 0 0 42px;
  text-align: right;
  padding-right: 10px;
  opacity: 0.45;
  user-select: none;
  font-variant-numeric: tabular-nums;
}
.marker {
  flex: 0 0 18px;
  text-align: center;
  opacity: 0.7;
  user-select: none;
}
.line-content { flex: 1; }
.diff-add { background: color-mix(in srgb, var(--ud-green) 38%, transparent); border-radius: 3px; }
.diff-del {
  background: color-mix(in srgb, var(--ud-red) 38%, transparent);
  border-radius: 3px;
  text-decoration: line-through;
  text-decoration-thickness: 1px;
}
.diff-equal {}
.diff-blank { opacity: 0.3; }
@media (prefers-reduced-motion: reduce) {
  .diff-pane { scroll-behavior: auto; }
  .ruler-mark { transition: none; }
}
"""

# Short Pygments token classes (see syntax.token_css_class), prefixed "hl-"
# and grouped by color so multiple related token kinds share a rule.
SYNTAX_CSS = """
.hl-k, .hl-kc, .hl-kd, .hl-kn, .hl-kp, .hl-kr, .hl-kt, .hl-ow { color: #c678dd; font-weight: 600; }
.hl-s, .hl-s1, .hl-s2, .hl-sa, .hl-sb, .hl-sc, .hl-sd, .hl-se, .hl-sh, .hl-si, .hl-sx, .hl-sr, .hl-ss, .hl-dl { color: #98c379; }
.hl-c, .hl-c1, .hl-cm, .hl-cp, .hl-cpf, .hl-ch, .hl-cs { color: #7f848e; font-style: italic; }
.hl-m, .hl-mb, .hl-mf, .hl-mh, .hl-mi, .hl-mo, .hl-il { color: #d19a66; }
.hl-nf, .hl-fm { color: #61afef; }
.hl-nc, .hl-vc { color: #e5c07b; }
.hl-nb, .hl-bp { color: #56b6c2; }
.hl-nd, .hl-ne, .hl-nt { color: #e06c75; }
.hl-na { color: #d19a66; }
.hl-err { color: #e06c75; text-decoration: underline wavy; }
"""

ALL_CSS = DIFF_CSS + SYNTAX_CSS

# App chrome only (not in the HTML export): instant press feedback, a translucent header that
# content scrolls under, the logo gradient on the primary action, and card-like metrics.
APP_CSS = """
[data-testid="stHeader"] {
  background: light-dark(rgba(255, 255, 255, 0.72), rgba(14, 18, 24, 0.72));
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}
[data-testid="stCaption"] { letter-spacing: 0.01em; }
h1, h2, h3 { letter-spacing: -0.02em; }
button[data-testid^="stBaseButton"] {
  transition: transform 100ms ease-out, filter 120ms ease-out, box-shadow 120ms ease-out;
}
button[data-testid^="stBaseButton"]:active { transform: scale(0.97); }
button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(90deg, var(--ud-red), var(--ud-green));
  border: none;
  color: #0E1218;
  font-weight: 650;
  box-shadow: 0 2px 10px color-mix(in srgb, var(--ud-green) 30%, transparent);
}
button[data-testid="stBaseButton-primary"]:hover {
  filter: brightness(1.06) saturate(1.1);
  color: #0E1218;
  box-shadow: 0 4px 16px color-mix(in srgb, var(--ud-green) 38%, transparent);
}
[data-testid="stMetric"] {
  background: light-dark(#F1F4F8, #1A202B);
  border: 1px solid var(--ud-line);
  border-radius: 14px;
  padding: 14px 18px;
}
[data-testid="stTextArea"] textarea {
  font-family: ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, monospace;
  font-size: 0.85rem;
}
@media (prefers-reduced-motion: reduce) {
  button[data-testid^="stBaseButton"] { transition: none; }
  button[data-testid^="stBaseButton"]:active { transform: none; }
}
@media (prefers-reduced-transparency: reduce) {
  [data-testid="stHeader"] { background: light-dark(#FFFFFF, #0E1218); backdrop-filter: none; -webkit-backdrop-filter: none; }
}
"""

DIFF_CSS = """
.diff-container { display: flex; gap: 12px; }
.diff-column { flex: 1; min-width: 0; }
.diff-pane {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.85rem;
  border: 1px solid rgba(128, 128, 128, 0.3);
  border-radius: 6px;
  overflow: auto;
  max-height: 600px;
}
.diff-row {
  display: flex;
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1px 6px;
  line-height: 1.4;
}
.diff-row.row-delete { background: rgba(248, 81, 73, 0.12); }
.diff-row.row-insert { background: rgba(46, 160, 67, 0.12); }
.line-no {
  flex: 0 0 42px;
  text-align: right;
  padding-right: 8px;
  opacity: 0.5;
  user-select: none;
}
.marker {
  flex: 0 0 18px;
  text-align: center;
  opacity: 0.7;
  user-select: none;
}
.line-content { flex: 1; }
.diff-add { background: rgba(46, 160, 67, 0.45); border-radius: 2px; }
.diff-del {
  background: rgba(248, 81, 73, 0.45);
  border-radius: 2px;
  text-decoration: line-through;
  text-decoration-thickness: 1px;
}
.diff-equal {}
.diff-blank { opacity: 0.3; }
"""

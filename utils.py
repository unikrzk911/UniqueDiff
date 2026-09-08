import re


def read_uploaded_file(uploaded_file):
    """Decode an st.file_uploader UploadedFile to text, tolerating odd encodings."""
    raw = uploaded_file.getvalue()
    for encoding in ('utf-8', 'utf-8-sig', 'latin-1'):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', errors='replace')


def normalize_text(text, ignore_whitespace=False, ignore_case=False,
                    ignore_line_endings=False, ignore_blank_lines=False):
    if ignore_line_endings:
        text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    if ignore_blank_lines:
        lines = [line for line in lines if line.strip() != '']
    if ignore_whitespace:
        lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    text = '\n'.join(lines)
    if ignore_case:
        text = text.lower()
    return text


def count_stats(text):
    return {
        'chars': len(text),
        'words': len(text.split()),
        'lines': len(text.splitlines()) if text else 0,
    }

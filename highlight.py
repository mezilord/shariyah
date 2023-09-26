import re

#it returns the highlighted text in html format
def highlight_text(data, text_to_highlight):
    highlighted_text = re.sub(r'(?i)\b{}\b'.format(
        text_to_highlight), r'<span style="color: red;">{}</span>'.format(text_to_highlight), data)
    return highlighted_text


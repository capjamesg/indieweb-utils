import re

FIRST_REFERENCE = r"\[(\d+)\]"
FOOTNOTE_REFERNECE = r"\[\^(\d+)\]"


def add_footnote_links(text: str, add_sup: bool = False) -> str:
    """
    Add HTML footnotes to text.

    Footnotes are defined with [int] and referenced with [^int].

    :param text: Text to add footnotes to
    :return: Text with footnotes added

    Example:

        from indieweb_utils import add_footnote_links

        text = 'This is a footnote [1] and this is a reference [^1].'

        print(add_footnote_links(text))
    """

    # raise warning if footnote is not defined
    for footnote in re.findall(FIRST_REFERENCE, text):
        print("Warning: footnote " + footnote + " is not defined.")
        if footnote not in re.findall(FOOTNOTE_REFERNECE, text):
            print("Warning: footnote " + footnote + " is not defined.")

        if add_sup:
            text = re.sub(FIRST_REFERENCE, r'<sup><a href="#fn:\1" id="fnref:\1">\1</a></sup>', text)
        else:
            text = re.sub(FIRST_REFERENCE, r'<a href="#fn:\1" id="fnref:\1">\1</a>', text)

    # look for [int] and replace with link to footnote
    if add_sup:
        text = re.sub(FOOTNOTE_REFERNECE, r'<sup><a href="#fnref:\1" id="fn:\1">\1</a></sup>', text)
    else:
        text = re.sub(FOOTNOTE_REFERNECE, r'<a href="#fnref:\1" id="fn:\1">\1</a>', text)

    return text

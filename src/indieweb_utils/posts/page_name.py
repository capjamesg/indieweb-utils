import mf2py
import requests
from bs4 import BeautifulSoup

from ..parsing.parse import RequestError, get_soup


def get_page_name(url: str, html: str = None, soup: BeautifulSoup = None) -> str:
    """
    Retrieve the name of a page using the Page Name Discovery algorithm.

    :refs: https://indieweb.org/page-name-discovery

    :param url: The url of the page whose title you want to retrieve.
    :type url: str
    :param html: The HTML of the page whose title you want to retrieve.
    :type html: str
    :return: A representative "name" for the page.
    :rtype: str

    Example:

    .. code-block:: python

        import indieweb_utils

        page_name = indieweb_utils.get_page_name("https://jamesg.blog")

        print(page_name) # "Home | James' Coffee Blog"
    """

    parsed_mf2_tree = None

    if html:
        soup = get_soup(html)

    if soup is None:
        try:
            contents = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            raise RequestError("Request to retrieve URL did not return a valid response.")

        soup = BeautifulSoup(contents.text, "html.parser")

        html = contents.text

    parsed_mf2_tree = mf2py.parse(doc=html)

    # only search the top level of the tree
    # representative h-entries, which is what this function looks for, should not be lower down
    for item in parsed_mf2_tree["items"]:
        if item["type"][0] != "h-entry":
            continue

        name = item["properties"].get("name")

        if name and len(name) > 0:
            return name[0]

        summary = item["properties"].get("summary")

        if summary and len(summary) > 0:
            return summary[0]

    page_title = soup.title

    if page_title:
        return page_title.text

    return "Untitled"

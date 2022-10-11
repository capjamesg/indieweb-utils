from dataclasses import dataclass
from typing import Any, Dict

import mf2py
from bs4 import BeautifulSoup

import requests
from ..parsing import get_soup, RequestError


def get_page_name(url: str, html: str, soup: BeautifulSoup = None) -> Dict[str, Any]:
    """
    Retrieve the name of a page using the Page Name Discovery algorithm.

    :refs: https://indieweb.org/page-name-discovery

    :param url: The url of the page whose title you want to retrieve.
    :type url: str
    :param html: The HTML of the page whose title you want to retrieve.
    :type html: str
    :return: A representative "name" for the page.
    :rtype: str
    """

    if html:
        soup = get_soup(html)
    elif soup is not None:
        try:
            contents = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            raise RequestError("Request to retrieve URL did not return a valid response.")

        soup = BeautifulSoup(contents.text, "html.parser")

    if html:
        parsed_mf2_tree = mf2py.parse(doc=html)
    else:
        parsed_mf2_tree = mf2py.parse(doc=contents.text)

    # only search the top level of the tree
    # representative h-entries, which is what this function looks for, should not be lower down
    for item in parsed_mf2_tree["items"]:
        if item["type"][0] != "h-entry":
            continue

        name = item["properties"].get("name")

        if name:
            return name

        summary = item["properties"].get("summary")

        if summary:
            return summary

    page_title = soup.title

    if page_title:
        return page_title.string

    return "Untitled"

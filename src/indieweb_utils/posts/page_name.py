from dataclasses import dataclass
from typing import Any, Dict
from bs4 import BeautifulSoup

from ..parsing import get_soup

import mf2py


class RepresentativeHCardParsingError(Exception):
    pass


@dataclass
class RepresentativeHCard:
    # TODO: Fill this out with a full h-card object
    pass


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
        soup = get_soup(url=url)

    if html:
        parsed_mf2_tree = mf2py.parse(doc=html)
    
    return None
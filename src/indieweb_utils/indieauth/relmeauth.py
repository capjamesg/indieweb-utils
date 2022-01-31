from typing import List
from urllib.parse import urlparse as parse_url

import mf2py
import requests
from bs4 import BeautifulSoup

from ..utils.urls import canonicalize_url


def get_valid_relmeauth_links(url: str) -> List[str]:
    """
    Get the valid links on a page that point back to a rel=me URL per RelMeAuth.

    refs: https://indieweb.org/RelMeAuth
    refs: http://microformats.org/wiki/RelMeAuth

    :url: The url to parse.
    :type url: str
    :return: The valid relmeauth links.
    :rtype: dict
    """
    domain = parse_url(url).netloc

    canonical_url = canonicalize_url(url, domain)

    mf2_data = mf2py.parse(url=canonical_url)

    rel_me_links = mf2_data["rels"].get("me", [])

    valid_rel_me_links = []

    for link in rel_me_links:
        try:
            link_valid = requests.get(link, timeout=5)
        except requests.exceptions.RequestException:
            continue

        if link_valid.status_code != 200:
            continue

        parsed_page = BeautifulSoup(link_valid.text, "html.parser")

        page_links = parsed_page.find_all("a") + parsed_page.find_all("link")

        for item in page_links:
            # check if link is a rel me link
            # if it is, add the link to the list of valid rel me links

            if not item.get("rel"):
                continue
            
            if not "me" in item.get("rel"):
                continue

            if item == canonical_url:
                valid_rel_me_links.append(link)
                continue

    return valid_rel_me_links

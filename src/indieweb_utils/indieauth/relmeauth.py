from typing import List, Set
from urllib.parse import urlparse as parse_url

import mf2py
import requests
from bs4 import BeautifulSoup

from ..parsing.parse import get_parsed_mf2_data
from ..utils.urls import canonicalize_url


def get_valid_relmeauth_links(
    url: str, require_rel_me_link_back: bool = True, html: str = None, parsed_mf2: mf2py.Parser = None
) -> List[str]:
    """
    Get the valid links on a page that point back to a rel=me URL per RelMeAuth.

    refs: https://indieweb.org/RelMeAuth
    refs: http://microformats.org/wiki/RelMeAuth

    :url: The url to parse.
    :type url: str
    :require_rel_me_link_back: Whether to require a rel=me link back to the specified URL.
        If this property is set to False, this function will return all sites that link back
        to the specified URL, even if they do not have a rel=me attribute. If this property is
        set to True (the default), this function will only return sites that have a rel=me link
        pointing back to your URL.
    :type require_rel_me_link_back: bool
    :return: The valid relmeauth links.
    :rtype: dict

    Example:

    .. code-block:: python

        import indieweb_utils

        url = "https://jamesg.blog"

        valid_relmeauth_links = indieweb_utils.get_valid_relmeauth_links(url)

        for link in valid_relmeauth_links:
            print(link)
    """

    domain = parse_url(url).netloc

    canonical_url = canonicalize_url(url, domain).strip("/")

    mf2_data = get_parsed_mf2_data(parsed_mf2, html, canonical_url)

    rel_me_links = [canonicalize_url(url, domain) for url in mf2_data["rels"].get("me", [])]

    valid_rel_me_links: Set[str] = set()

    if require_rel_me_link_back is False:
        return list(set(rel_me_links))

    for link in rel_me_links:
        try:
            link_valid = requests.get(link, timeout=5)
        except requests.exceptions.RequestException:
            continue

        if link_valid.status_code != 200:
            continue

        parsed_page = BeautifulSoup(link_valid.text, "html.parser")

        page_links = parsed_page.find_all("a") + parsed_page.find_all("link")

        link_domain = parse_url(link).netloc

        for item in page_links:
            # check if link is a rel me link
            # if it is, add the link to the list of valid rel me links

            if not item.get("rel") and require_rel_me_link_back is True:
                continue

            if "me" not in item.get("rel", "") and require_rel_me_link_back is True:
                continue

            if item.get("href") == canonical_url:
                canonical_link = canonicalize_url(link, link_domain)

                valid_rel_me_links.add(canonical_link)

    return list(valid_rel_me_links)

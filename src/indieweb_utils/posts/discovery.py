import re
from typing import List, Tuple
from urllib import parse as url_parse

import mf2py
import requests
from bs4 import BeautifulSoup

from ..parsing.parse import get_parsed_mf2_data, get_soup
from ..utils.urls import _is_http_url, canonicalize_url

# This regex identifies permashortlink citations in the form of (example.com slug)
# Permashortlink citations may be used as a link to a post that does not contain a hyperlink
# Checking for a permashortlink citation is a step in the Original Post Discovery algorithm
# More on permashortlink citations: https://indieweb.org/permashortcitation
PERMASHORTLINK_CITATION_BRACKET_MATCHING = r"\((.*?)\)"


class PostDiscoveryError(Exception):
    pass


class PostTypeFormattingError(Exception):
    pass


def _process_candidate_url(candidate_url: str, posse_permalink: str, parsed_post: BeautifulSoup) -> str:
    try:
        request = requests.get(candidate_url, timeout=5)
    except requests.exceptions.RequestException:
        raise PostDiscoveryError("Could not get candidate url")

    parsed_candidate_url = BeautifulSoup(request.text, "lxml")

    all_hyperlinks = parsed_candidate_url.select("a")

    posse_domain = url_parse.urlsplit(posse_permalink).netloc

    for link in all_hyperlinks:
        if "u-syndication" in link.get("class"):
            url_to_check = link.get("href")

            original_post_url = _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain)

            if original_post_url:
                return original_post_url

    all_syndication_link_headers = parsed_post.select("link[rel='syndication']")

    for header in all_syndication_link_headers:
        if header.get("href") == posse_permalink:
            url_to_check = header.get("href")

            original_post_url = _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain)

            if original_post_url:
                return original_post_url

    return ""


def _check_for_link_in_post(last_text: BeautifulSoup) -> str:
    last_text = last_text[0].select("p")[-1]

    # if permashortlink citation
    # format = (url.com id)

    permashortlink_citation = re.search(PERMASHORTLINK_CITATION_BRACKET_MATCHING, last_text.text)

    if permashortlink_citation is not None:
        permashortlink = re.search(PERMASHORTLINK_CITATION_BRACKET_MATCHING, last_text.text)

    if permashortlink is not None:
        permashortlink_value = "http://" + permashortlink.group(0) + "/" + permashortlink.group(1)

        candidate_url = permashortlink_value
    else:
        # check for url at end
        split_text = last_text.text.split(" ")

        if _is_http_url(split_text[-1]):
            candidate_url = split_text[-1]
        else:
            candidate_url = ""

    return candidate_url


def discover_original_post(posse_permalink: str, soup: BeautifulSoup = None, html: str = "") -> str:
    """
    Find the original version of a post per the Original Post Discovery algorithm.

    refs: https://indieweb.org/original-post-discovery#Algorithm

    :param posse_permalink: The permalink of the post.
    :type posse_permalink: str
    :return: The original post permalink.
    :rtype: str

    Example:

    .. code-block:: python

        import indieweb_utils

        original_post_url = indieweb_utils.discover_original_post("https://example.com")

        print(original_post_url)

    :raises PostDiscoveryError: A candidate URL cannot be retrieved or when a specified
        post is not marked up with h-entry.
    """

    if soup is None:
        parsed_post = get_soup(html, posse_permalink)
    else:
        parsed_post = soup

    # Get the post h-entry

    post_h_entry = parsed_post.select(".h-entry")

    original_post_url = None

    if not post_h_entry:
        raise PostDiscoveryError("Could not find h-entry")

    post_h_entry = post_h_entry[0]

    # select with u-url and u-uid
    if post_h_entry.select(".u-url .u-uid"):
        original_post_url = post_h_entry.select(".u-url .u-uid")[0].get("href")
        return original_post_url

    canonical_links = parsed_post.select("link[rel='canonical']")

    if canonical_links:
        original_post_url = canonical_links[0].get("href")
        return original_post_url

    # look for text with see original anchor text

    for link in parsed_post.select("a"):
        if link.text.lower() == "see original".lower() and link.get("href"):
            original_post_url = link.get("href")

            return original_post_url

    candidate_url = None

    last_text = post_h_entry.select(".e-content")

    if last_text:
        candidate_url = _check_for_link_in_post(last_text)

    if candidate_url and candidate_url != "":
        post_url = _process_candidate_url(candidate_url, posse_permalink, parsed_post)

        if post_url != "":
            return post_url

    return ""


def _discover_h_card_from_author_page(author_url: str, rel_author: str) -> dict:
    new_h_card = mf2py.parse(url=author_url)

    # get rel me values from parsed object
    if new_h_card.get("rels") and new_h_card.get("rels").get("me"):
        rel_mes = new_h_card["rels"]["me"]
    else:
        rel_mes = []

    final_h_card = [e for e in new_h_card["items"] if e["type"] == "h-card"]

    for card in final_h_card:
        for j in card["items"]:
            if (
                j.get("type")
                and j.get("type") == ["h-card"]
                and j["properties"]["url"] == rel_author
                and j["properties"].get("uid") == j["properties"]["url"]
            ):
                h_card = j
                return h_card

            if j.get("type") and j.get("type") == ["h-card"] and j["properties"].get("url") in rel_mes:
                h_card = j
                return h_card

            if j.get("type") and j.get("type") == ["h-card"] and j["properties"]["url"] == rel_author:
                h_card = j
                return h_card

    return {}


def discover_author(url: str, html: str = "", parsed_mf2: mf2py.Parser = None) -> dict:
    """
    Discover the author of a post per the IndieWeb Authorship specification.

    :refs: https://indieweb.org/authorship-spec

    :param url: The URL of the post.
    :type url: str
    :param page_contents: The optional page contents to use.
        Specifying this value prevents a HTTP request being made to the URL.
    :type page_contents: str
    :return: A h-card of the post.
    :rtype: dict

    .. code-block:: python

        import indieweb_utils
        import mf2py

        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"

        parsed_mf2 = mf2py.parse(url=url)

        post_author = indieweb_utils.discover_author(
            h_entry
        )

        print(post_author) # A h-card object representing the post author.
    """

    full_page = get_parsed_mf2_data(parsed_mf2, html, url)

    preliminary_author = None

    h_entry = [e for e in full_page["items"] if e["type"] == ["h-entry"]]

    if h_entry and h_entry[0]["properties"].get("author"):
        preliminary_author = h_entry[0]["properties"]["author"][0]

    h_feed = [e for e in full_page["items"] if e["type"] == ["h-feed"]]

    if h_feed and h_feed[0]["properties"].get("author"):
        preliminary_author = h_entry[0]["properties"]["author"][0]

    author_page_url = None

    if preliminary_author and type(preliminary_author) == str:
        if preliminary_author.startswith("https://"):
            # author is url, further processing needed
            author_page_url = preliminary_author
        else:
            # author is name
            return {
                "type": ["h-card"],
                "properties": {
                    "name": [preliminary_author],
                    "url": [url],
                },
            }

    if preliminary_author and type(preliminary_author) == dict:
        # author is h-card so the value can be returned
        return preliminary_author

    # if rel=author, look for h-card on the rel=author link
    if author_page_url is None and h_entry and h_entry[0].get("rels") and h_entry[0]["rels"].get("author"):
        rel_author = h_entry[0]["rels"]["author"]

        if rel_author:
            author_page_url = rel_author[0]

    # canonicalize author page
    if author_page_url:
        domain = url_parse.urlsplit(url).netloc

        author_url = canonicalize_url(author_page_url, domain)

        h_card = _discover_h_card_from_author_page(author_url, rel_author)

        return h_card

    return {}


def get_post_type(h_entry: dict = {}, custom_properties: List[Tuple[str, str]] = []) -> str:
    """
    Return the type of a h-entry per the Post Type Discovery algorithm.

    :param h_entry: The h-entry whose type to retrieve.
    :type h_entry: dict
    :param custom_properties: The optional custom properties to use for the Post Type Discovery algorithm.
    :type custom_properties: list[tuple[str, str]]
    :return: The type of the h-entry.
    :rtype: str

    Here is an example of the function in action:

    .. code-block:: python

        import indieweb_utils
        import mf2py

        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"

        parsed_mf2 = mf2py.parse(url=url)

        h_entry = [e for e in parsed_mf2["items"] if e["type"] == ["h-entry"]][0]

        post_type = indieweb_utils.get_post_type(
            h_entry
        )

        print(post_type) # article

    :raises PostTypeFormattingError: Raised when you specify a custom_properties tuple in the wrong format.
    """

    post = h_entry.get("properties")

    if post is None:
        return "unknown"

    values_to_check = [
        ("rsvp", "rsvp"),
        ("in-reply-to", "reply"),
        ("repost-of", "repost"),
        ("like-of", "like"),
        ("video", "video"),
        ("photo", "photo"),
        ("summary", "summary"),
    ]

    for prop in custom_properties:
        if len(prop) == 2 and isinstance(prop, tuple) and isinstance(prop[0], str) and isinstance(prop[1], str):
            values_to_check.append(prop)
        else:
            raise PostTypeFormattingError("custom_properties must be a list of tuples")

    for item in values_to_check:
        if post.get(item[0]):
            return item[1]

    post_type = "note"

    if post.get("name") is None or post.get("name")[0] == "":
        return post_type

    title = post.get("name")[0].strip().replace("\n", " ").replace("\r", " ")

    # Default should be a list so we're never dealing with None
    content = post.get("content", [])

    if content:
        # Default should be an empty string, so we're never dealing with None
        text = content[0].get("text", "")
        html = content[0].get("html", "")

        if html or text:
            # Prefer to validate against html than text version of the content
            content_text = BeautifulSoup(html or text, "lxml").get_text()

            if content_text and not content_text.startswith(title):
                return "article"

    return post_type


def _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain):
    if url_to_check == posse_permalink:
        return candidate_url

    if url_to_check and url_parse.urlsplit(url_to_check).netloc == posse_domain:
        try:
            r = requests.get(url_to_check, timeout=10, allow_redirects=True)
        except requests.exceptions.RequestException:
            # handler will prevent exception due to timeout, if one occurs
            pass

        for url_item in r.history:
            if url_item.url == posse_permalink:
                return candidate_url

    return None

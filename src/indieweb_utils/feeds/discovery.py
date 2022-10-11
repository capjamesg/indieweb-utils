import dataclasses
from typing import Dict, List, Optional, Tuple
from urllib import parse as url_parse

import mf2py
import requests
from bs4 import BeautifulSoup

from ..utils.urls import _is_http_url, canonicalize_url
from ..webmentions.discovery import _find_links_in_headers


@dataclasses.dataclass
class FeedUrl:
    url: str
    mime_type: str
    title: str


def _get_page_feed_contents(url: str, html: str) -> Tuple[requests.Response, str]:
    if html:
        try:
            web_page_request = requests.head(url, timeout=10, allow_redirects=True)
        except requests.RequestException:
            raise Exception("Request to retrieve URL did not return a valid response.")

    if not html:
        try:
            web_page_request = requests.get(url, timeout=10, allow_redirects=True)
        except requests.RequestException:
            raise Exception("Request to retrieve URL did not return a valid response.")
        else:
            html = web_page_request.text

    return web_page_request, html


def discover_web_page_feeds(url: str, user_mime_types: Optional[List[str]] = None, html: str = "") -> List[FeedUrl]:
    """
    Get all feeds on a web page.

    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    :param user_mime_types: A list of mime types whose associated feeds you want to retrieve.
    :type user_mime_types: Optional[List[str]]
    :param html: A string with the HTML on a page.
    :type html: str
    :return: A list of FeedUrl objects.
    :rtype: List[FeedUrl]

    Example:

    .. code-block:: python

        import indieweb_utils

        url = "https://jamesg.blog/"

        feeds = indieweb_utils.discover_web_page_feeds(url)

        # print the url of all feeds to the console
        for f in feeds:
            print(f.url)
    """
    user_mime_types = user_mime_types or []

    if not _is_http_url(url):
        url = "https://" + url
    elif url.startswith("//"):
        url = "https:" + url

    web_page_request, html = _get_page_feed_contents(url, html)

    soup = BeautifulSoup(html, "lxml")

    # check for presence of mf2 hfeed
    h_feed = soup.find_all(class_="h-feed")
    page_title = soup.find("title")

    page_domain = url_parse.urlsplit(url).netloc

    valid_mime_types = {
        "application/rss+xml",
        "application/atom+xml",
        "application/rdf+xml",
        "application/xml",
        "application/json",
        "application/mf2+json",
        "application/atom+xml",
        "application/feed+json",
        "application/jf2feed_json",
    }

    feeds: List[FeedUrl] = []

    for mime_type in valid_mime_types.union(user_mime_types):
        if soup.find("link", rel="alternate", type=mime_type):
            feed_title = soup.find("link", rel="alternate", type=mime_type).get("title")
            feed_url = canonicalize_url(soup.find("link", rel="alternate", type=mime_type).get("href"), page_domain)

            feeds.append(FeedUrl(url=feed_url, mime_type=mime_type, title=feed_title))

    if h_feed:
        feeds.append(FeedUrl(url=url, mime_type="text/html", title=page_title.text))

    http_headers = _find_links_in_headers(headers=web_page_request.headers, target_headers=["alternate", "feed"])

    for rel, item in http_headers.items():
        feed_mime_type = item.get("mime_type", "")

        feed_title = http_headers.get(rel, "")
        feed_url = canonicalize_url(url, page_domain)

        feeds.append(FeedUrl(url=feed_url, mime_type=feed_mime_type, title=feed_title))

    return feeds


def discover_h_feed(url: str, html: str = "") -> Dict:
    """
    Find the main h-feed that represents a web page as per the h-feed Discovery algorithm.

    refs: https://microformats.org/wiki/h-feed#Discovery

    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    :param html: The HTML of a page whose feeds you want to retrieve
    :type html: str
    :return: The h-feed data.
    :rtype: dict

    Example:

    .. code-block:: python

        import indieweb_utils

        url = "https://jamesg.blog/"

        hfeed = indieweb_utils.discover_h_feed(url)

        print(hfeed)
    """

    if html:
        parsed_main_page_mf2 = mf2py.parse(doc=html)
    else:
        parsed_main_page_mf2 = mf2py.parse(url=url)

    all_page_feeds = discover_web_page_feeds(url)

    get_mf2_feed = [feed for feed in all_page_feeds if feed.mime_type == "text/mf2+html"]

    if len(get_mf2_feed) > 0:
        feed = get_mf2_feed[0].url

        parsed_feed = mf2py.parse(url=feed)

        h_feed = [item for item in parsed_feed["items"] if item.get("type") and item.get("type")[0] == "h-feed"]

        if h_feed:
            return h_feed[0]

    h_feed = [item for item in parsed_main_page_mf2["items"] if item.get("type") and item.get("type")[0] == "h-feed"]

    if h_feed:
        return h_feed[0]

    return {}

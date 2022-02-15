import dataclasses
from typing import List, Optional
from urllib import parse as url_parse

import mf2py
import requests
from bs4 import BeautifulSoup

from ..utils.urls import _is_http_url, canonicalize_url


@dataclasses.dataclass
class FeedUrl:
    url: str
    mime_type: str
    title: str


def discover_web_page_feeds(url: str, user_mime_types: Optional[List[str]] = None) -> List[FeedUrl]:
    """
    Get all feeds on a web page.
    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    """
    user_mime_types = user_mime_types or []

    if not _is_http_url(url):
        url = "https://" + url
    elif url.startswith("//"):
        url = "https:" + url
    try:
        web_page_request = requests.get(url, timeout=10, allow_redirects=True)

        web_page = web_page_request.text
    except requests.exceptions.RequestException:
        return []

    soup = BeautifulSoup(web_page, "lxml")

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

    return feeds


def discover_h_feed(url: str) -> dict:
    """
    Find the main h-feed that represents a web page as per the h-feed Discovery algorithm.

    refs: https://microformats.org/wiki/h-feed#Discovery

    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    :return: The h-feed data.
    :rtype: dict
    """

    parsed_main_page_mf2 = mf2py.parse(url=url)

    all_page_feeds = discover_web_page_feeds(url)

    get_mf2_feed = [feed for feed in all_page_feeds if feed.mime_type == "text/mf2+html"]

    if len(get_mf2_feed) > 0:
        feed = get_mf2_feed[0].url

        parsed_feed = mf2py.parse(url=feed)

        h_feed = [item for item in parsed_feed["items"] if item.get("type", [])[0] == "h-feed"]

        if h_feed:
            return h_feed[0]

    h_feed = [item for item in parsed_main_page_mf2["items"] if item.get("type", [])[0] == "h-feed"]

    if h_feed:
        return h_feed[0]

    return {}




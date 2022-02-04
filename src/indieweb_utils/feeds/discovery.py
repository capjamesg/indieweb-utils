import dataclasses
from typing import List, Optional
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup

from ..utils.urls import _is_http_url, canonicalize_url
from ..webmentions.discovery import _find_links_in_headers


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

    http_headers = _find_links_in_headers(headers=web_page_request.headers, target_headers=["alternate", "feed"])

    for rel, item in http_headers.items():
        feed_mime_type = item.get("mime_type", "")

        feed_title = http_headers.get(rel, "")
        feed_url = canonicalize_url(url, page_domain)

        feeds.append(FeedUrl(url=feed_url, mime_type=feed_mime_type, title=feed_title))

    return feeds

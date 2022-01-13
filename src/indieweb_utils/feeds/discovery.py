import dataclasses
from typing import Dict, Optional, List
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup

from ..utils.urls import canonicalize_url


@dataclasses.dataclass
class FeedUrl:
    url: str
    mime_type: str
    title: str


def discover_web_page_feeds(url: str, user_mime_types: Optional[List[str]] = None) -> Dict[str, str]:
    """
    Get all feeds on a web page.
    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    :return: A dictionary of feeds on the web page. The dictionary keys are feed URLs and the values are feed titles.
    :rtype: dict
    """
    user_mime_types = user_mime_types or []

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    elif url.startswith("//"):
        url = "https:" + url

    try:
        web_page = requests.get(url, timeout=10, allow_redirects=True)

        web_page = web_page.text
    except:
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

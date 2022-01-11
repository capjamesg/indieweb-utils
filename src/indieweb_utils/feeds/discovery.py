import requests
from bs4 import BeautifulSoup


def discover_web_page_feeds(url):
    """
    Get all feeds on a web page.

    :param url: The URL of the page whose associated feeds you want to retrieve.
    :type url: str
    :return: A dictionary of feeds on the web page. The dictionary keys are feed URLs and the values are feed titles.
    :rtype: dict
    """
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

    feeds = []

    if soup.find("link", rel="alternate", type="application/atom+xml"):
        feeds.append(soup.find("link", rel="alternate", type="application/atom+xml").get("href"))
    if soup.find("link", rel="alternate", type="application/rss+xml"):
        feeds.append(soup.find("link", rel="alternate", type="application/rss+xml").get("href"))
    if soup.find("link", rel="feed", type="text/html"):
        # used for mircoformats rel=feed discovery
        feeds.append(soup.find("link", rel="feed", type="text/html").get("href"))
    if h_feed:
        feeds.append(url)

    for feed in range(len(feeds)):
        f = feeds[feed]

        if f.startswith("/"):
            feeds[feed] = url.strip("/") + f
        elif f.startswith("http://") or f.startswith("https://"):
            pass
        elif f.startswith("//"):
            feeds[feed] = "https:" + f

    return feeds

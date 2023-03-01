import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from urllib.parse import urlparse

from indieweb_utils import canonicalize_url

# from ..utils.urls import canonicalize_url

class TrackbackError(Exception):
    """Base class for trackback errors."""
    pass

class ConnectionError(TrackbackError):
    """Raised when a connection error occurs."""
    pass

class InvalidStatusCodeError(TrackbackError):
    """Raised when the server returns an invalid status code."""
    pass

def rsd_trackback_discovery(url: str):
    return rsd_discovery(url, "trackback:ping")

def rsd_discovery(url: str, attribute: str):
    """Discover an RSD attribute from a URL.

    :param url: The URL to discover the RSD attribute from.
    :param attribute: The attribute to discover.
    :returns: The value of the attribute.
    """

    get_rsd_request = requests.get(url)

    if get_rsd_request.status_code != 200:
        raise InvalidStatusCodeError("The server returned a status code of {}.".format(get_rsd_request.status_code))
    
    soup = BeautifulSoup(get_rsd_request.text, "html.parser")

    rsd = soup.find("link", rel="EditURI")

    if not rsd:
        return ""

    get_rsd_request = requests.get(rsd.get("href"))

    if get_rsd_request.status_code != 200:
        raise InvalidStatusCodeError("The server returned a status code of {}.".format(get_rsd_request.status_code))
    
    soup = BeautifulSoup(get_rsd_request.text, "html.parser")

    trackback_url = soup.find(attribute)

    if not trackback_url:
        return ""
    
    domain = urlparse(url).netloc

    return canonicalize_url(trackback_url.text, domain)

def discover_trackback_url(url: str):
    """Discover the trackback URL from a URL.
    
    :param url: The URL to discover the trackback URL from.
    :returns: The trackback URL.
    """

    get_trackback_url_request = requests.get(url)

    if get_trackback_url_request.status_code != 200:
        raise InvalidStatusCodeError("The server returned a status code of {}.".format(get_trackback_url_request.status_code))
    
    soup = BeautifulSoup(get_trackback_url_request.text, "html.parser")

    # get all comments
    comments = soup.find_all(string=lambda text:isinstance(text, Comment))

    for c in comments:
        soup = BeautifulSoup(c, "lxml")
        
        rdf = soup.find("rdf:description")

        if not rdf:
            continue

        trackback_url = rdf.get("trackback:ping")

        if not trackback_url:
            raise TrackbackError("No trackback URL found in RDF.")
        
        domain = urlparse(url).netloc

        return canonicalize_url(trackback_url, domain)

    trackback_url = rsd_trackback_discovery(url)

    if trackback_url:
        return trackback_url
    
    return ""


def send_trackback(target_url, source_url, title: str = None, excerpt: str = None, blog_name: str = None):
    """Send a trackback to a URL.

    :param target_url: The URL to send the trackback to.
    :param source_url: The URL of your post.
    :param title: The title of your post.
    :param excerpt: An excerpt of your post.
    :param blog_name: The name of your blog.
    :returns: The status code and message from the server.
    """

    try:
        send_trackback_request = requests.post(target_url, data={
            "url": source_url,
            "title": title,
            "excerpt": excerpt,
            "blog_name": blog_name
        }, headers={
            "User-Agent": "IndieWeb Utils",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        })
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not connect to the server.")
    
    if send_trackback_request.status_code != 200:
        raise InvalidStatusCodeError("The server returned a status code of {}.".format(send_trackback_request.status_code))
    
    soup = BeautifulSoup(send_trackback_request.text, "lxml")

    soup = soup.find("response")

    if not soup:
        raise TrackbackError("The server returned an invalid response.")

    if soup.find("error") and soup.find("error").text != "0":
        raise TrackbackError("The server returned an error: {}".format(soup.find("message").text))
    
new_trackback_url = discover_trackback_url("https://arxiv.org/abs/1706.03762/")

if new_trackback_url:
    send_trackback(new_trackback_url, "https://towardsdatascience.com/transformer-models-101-getting-started-part-1-b3a77ccfa14d/", title="", excerpt="", blog_name="")
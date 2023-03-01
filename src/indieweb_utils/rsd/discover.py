from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ..utils.urls import canonicalize_url


class InvalidStatusCodeError(Exception):
    """Raised when the server returns an invalid status code."""

    pass


def rsd_discovery(url: str, attribute: str):
    """Discover an RSD attribute from a URL.

    :param url: The URL to discover the RSD attribute from.
    :param attribute: The attribute to discover.
    :returns: The value of the attribute.

    Example:
        from indieweb.utils import rsd_discovery

        # discover the RSD document for a given URL
        rsd_discovery('http://example.com', 'trackback:ping')
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

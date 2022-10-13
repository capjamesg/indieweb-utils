import ipaddress
from dataclasses import dataclass
from typing import Dict, List
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup

from ..utils.urls import _is_http_url

_WEBMENTION = "webmention"  # TODO: Move this to a constants file


@dataclass
class WebmentionDiscoveryResponse:
    endpoint: str


class TargetNotProvided(Exception):
    pass


class WebmentionEndpointNotFound(Exception):
    pass


class UnacceptableIPAddress(Exception):
    """
    Raised if an IP address for a webmention endpoint does not resolve on the public internet.

    Local, loopback, private, reserved, and multicast IP addresses are not acceptable.
    """


class LocalhostEndpointFound(Exception):
    pass


def discover_webmention_endpoint(target: str) -> WebmentionDiscoveryResponse:
    """
    Return the webmention endpoint for the given target.

    :param target: The target to discover the webmention endpoint for.
    :type target: str
    :return: The discovered webmention endpoint.
    :rtype: str

    .. code-block:: python

        import indieweb_utils

        target = "https://jamesg.blog/"

        webmention_endpoint = indieweb_utils.discover_webmention_endpoint(
            target
        )

        print(webmention_endpoint) # https://webmention.jamesg.blog/webmention

    :raises TargetNotProvided: Target is not provided.
    :raises WebmentionEndpointNotFound: Webmention endpoint is not found.
    :raises UnacceptableIPAddress: Endpoint does not connect to an accepted IP.
    :raises LocalhostEndpointFound: Discovered endpoint is equal to localhost.
    """
    if not target:
        raise TargetNotProvided("No target provided.")

    endpoints = discover_endpoints(target, [_WEBMENTION])

    endpoint = endpoints.get("webmention", None)

    if endpoint is None:
        raise WebmentionEndpointNotFound("No webmention endpoint could be found for this resource.")

    # verify if IP address is not allowed
    try:
        endpoint_as_ip = ipaddress.ip_address(endpoint)

        if (
            endpoint.is_private is True
            or endpoint.is_multicast is True
            or endpoint_as_ip.is_loopback is True
            or endpoint_as_ip.is_unspecified is True
            or endpoint_as_ip.is_reserved is True
            or endpoint_as_ip.is_link_local is True
        ):
            raise UnacceptableIPAddress("The endpoint does not connect to an accepted IP address.")
    except ValueError:
        pass

    if endpoint == "localhost":
        raise LocalhostEndpointFound("The endpoint is localhost.")

    if endpoint == "":
        endpoint = target

    valid_starts = ("http://", "https://", "/")

    if not any(endpoint.startswith(valid_start) for valid_start in valid_starts):
        endpoint = "/".join(target.split("/")[:-1]) + "/" + endpoint

    if endpoint.startswith("/"):
        endpoint = "https://" + url_parse.urlsplit(target).scheme + endpoint

    return WebmentionDiscoveryResponse(endpoint=endpoint)


def discover_endpoints(url: str, headers_to_find: List[str], request: requests.Response = None):
    """
    Return a dictionary of specified endpoint locations for the given URL, if available.

    :param url: The URL to discover endpoints for.
    :type url: str
    :param headers_to_find: The headers to find.
        Values you may want to use include: microsub, micropub, token_endpoint,
        authorization_endpoint, subscribe.
    :type headers_to_find: dict[str, str]
    :return: The discovered endpoints.
    :rtype: dict[str, str]

    .. code-block:: python

        import indieweb_utils
        import requests

        url = "https://jamesg.blog/"

        # find the microsub rel link on a web page
        headers_to_find = ["microsub"]

        endpoints = indieweb_utils.discover_endpoints(
            url
        )

        print(endpoints) # {'microsub': 'https://aperture.p3k.io/'}

    :raises requests.exceptions.RequestException: Error raised while making the network request to discover endpoints.
    """
    response: Dict[str, str] = {}

    if request:
        endpoint_request = request
    else:
        try:
            endpoint_request = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            raise Exception("Could not connect to the specified URL.")

    link_headers = _find_links_in_headers(headers=endpoint_request.headers, target_headers=headers_to_find)

    for header in link_headers:
        response[header] = link_headers[header]["url"]

    response.update(_find_links_html(body=endpoint_request.text, target_headers=headers_to_find))
    return response


def _find_links_in_headers(*, headers, target_headers: List[str]) -> Dict[str, Dict[str, str]]:
    """Return a dictionary { rel: { url: 'url', mime_type: 'mime_type' } } containing the target headers."""
    found: Dict[str, Dict[str, str]] = {}
    links = headers.get("link")
    if links:
        # [{'url': 'https://micropub.jamesg.blog/micropub', 'rel': 'micropub'} ]
        parsed_link_headers: List[Dict[str, str]] = requests.utils.parse_header_links(links)
    else:
        return found

    for header in parsed_link_headers:
        url = header.get("url", "")
        rel = header.get("rel", "")
        mime_type = header.get("type", "")
        if _is_http_url(url) and rel in target_headers:
            found[rel] = {
                "url": url,
                "mime_type": mime_type,
            }

    # Add check for x-pingback header
    if "x-pingback" in target_headers:
        pingback_url = headers.get("x-pingback")

        if _is_http_url(pingback_url):
            # assign as "pingback" key in dictionary
            found["pingback"] = {
                "url": url,
                "mime_type": "",
            }

    return found


def _find_links_html(*, body: str, target_headers: List[str]) -> Dict[str, str]:
    soup = BeautifulSoup(body, "html.parser")
    found: Dict[str, str] = {}

    for link in soup.find_all("link"):
        try:
            rel = link.get("rel", [])[0]
            href = link.get("href")
        except IndexError:
            continue
        if _is_http_url(href) and rel in target_headers:
            found[rel] = href
    return found

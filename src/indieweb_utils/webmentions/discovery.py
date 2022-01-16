import ipaddress
from typing import Dict, List
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup

_WEBMENTION = "webmention"  # TODO: Move this to a constants file


def discover_webmention_endpoint(target):
    """
    Return the webmention endpoint for the given target.

    :param target: The target to discover the webmention endpoint for.
    :type target: str
    :return: The discovered webmention endpoint.
    :rtype: str
    """
    if not target:
        return None, "No target specified."

    endpoints = _discover_endpoints(target, [_WEBMENTION])

    endpoint = endpoints.get("webmention", None)

    if endpoint is None:
        message = "No webmention endpoint could be found for this resource."
        return None, message

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
            message = "The endpoint does not connect to an accepted IP address."
            return message, None
    except ValueError:
        pass

    if endpoint == "localhost":
        message = "This resource is not supported."
        return None, message

    if endpoint == "":
        endpoint = target

    valid_starts = ("http://", "https://", "/")

    if not any(endpoint.startswith(valid_start) for valid_start in valid_starts):
        endpoint = "/".join(target.split("/")[:-1]) + "/" + endpoint

    if endpoint.startswith("/"):
        endpoint = "https://" + url_parse.urlsplit(target).scheme + endpoint

    return endpoint, ""


def _discover_endpoints(url: str, headers_to_find: List[str]):
    """
    Return a dictionary of specified endpoint locations for the given URL, if available.

    :param url: The URL to discover endpoints for.
    :type url: str
    :param headers_to_find: The headers to find.
    :type headers_to_find: dict[str, str]
    :return: The discovered endpoints.
    :rtype: dict[str, str]
    """
    response: Dict[str, str] = {}

    endpoint_request = requests.get(url)

    response.update(_find_links_in_headers(headers=endpoint_request.headers, target_headers=headers_to_find))
    response.update(_find_links_html(body=endpoint_request.text, target_headers=headers_to_find))
    return response


def _find_links_in_headers(*, headers, target_headers: List[str]) -> Dict[str, str]:
    """Return a dictionary { rel: url } containing the target headers."""
    found: Dict[str, str] = {}
    links = headers.get("link")
    if links:
        # [{'url': 'https://micropub.jamesg.blog/micropub', 'rel': 'micropub'} ]
        parsed_link_headers: List[Dict[str, str]] = requests.utils.parse_header_links(links)
    else:
        return found

    for header in parsed_link_headers:
        url = header.get("url", "")
        rel = header.get("rel", "")
        if _is_http_url(url) and rel in target_headers:
            found[rel] = url
    return found


def _find_links_html(*, body: str, target_headers: List[str]) -> Dict[str, str]:
    """"""
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


def _is_http_url(url: str) -> bool:
    """
    Determine if URL is http or not
    """
    return url_parse.urlsplit(url).scheme in ["http", "https"]

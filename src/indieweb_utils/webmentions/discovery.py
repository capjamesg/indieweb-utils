import ipaddress
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup


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

    endpoints = _discover_endpoints(target, ["webmention"])

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


def _discover_endpoints(url, headers_to_find):
    """
    Return a dictionary of specified endpoint locations for the given URL, if available.

    :param url: The URL to discover endpoints for.
    :type url: str
    :param headers_to_find: The headers to find.
    :type headers_to_find: dict[str, str]
    :return: The discovered endpoints.
    :rtype: dict[str, str]
    """
    response = {}

    endpoint_request = requests.get(url)

    http_link_headers = endpoint_request.headers.get("link")

    if http_link_headers:
        parsed_link_headers = requests.utils.parse_header_links(http_link_headers.rstrip(">").replace(">,<", ",<"))
    else:
        parsed_link_headers = []

    for header in parsed_link_headers:
        if header["rel"] in headers_to_find:
            response[header["rel"]] = header["url"]

    soup = BeautifulSoup(endpoint_request.text, "lxml")

    for link in soup.find_all("link"):
        if link.get("rel") in headers_to_find:
            response[link.get("rel")] = link.get("href")

    for response_url in response:
        if not response[response_url].startswith("https://") and not response[response_url].startswith("http://"):
            response.pop(response_url)

    return response

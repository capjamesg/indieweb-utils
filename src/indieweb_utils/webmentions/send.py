from dataclasses import dataclass
from typing import List, Optional
from urllib import parse as url_parse

import requests

from ..utils.urls import _is_http_url
from . import discovery


@dataclass
class Header:
    name: str
    value: str


class MissingSourceError(Exception):
    pass


class MissingTargetError(Exception):
    pass


class UnsupportedProtocolError(Exception):
    """
    Raised if a provided webmention source or target uses a protocol other than http:// or https://.
    """

    pass


class TargetIsNotApprovedDomain(Exception):
    pass


class GenericWebmentionError(Exception):
    pass


class CouldNotConnectToWebmentionEndpoint(Exception):
    pass


@dataclass
class SendWebmentionResponse:
    title: str
    description: str
    url: str
    status_code: Optional[int]
    headers: List[Header]


def _validate_webmention(source: str, target: str):
    """
    Check if a webmention has a provided source, target, and valid protocol.
    """
    if not source:
        raise MissingSourceError("A source was not provided.")

    if not target:
        raise MissingTargetError("A target was not provided.")

    if not _is_http_url(source) or not _is_http_url(target):
        raise UnsupportedProtocolError("Only HTTP/HTTPS URLs are supported.")


def send_webmention(
    source: str,
    target: str,
    me: str = None,
    code: str = None,
    realm: str = None,
    target_webmention_endpoint: str = None,
) -> SendWebmentionResponse:
    """
    Send a webmention to a target URL.

    :param source: The source URL of the webmention.
    :type source: str
    :param target: The target URL to which you want to send the webmention.
    :type target: str
    :param me: The URL of the user.
    :type me: str
    :param code: An authorization code that grants access to the Webmention source (optional).
        See https://indieweb.org/Private-Webmention#Auth_Code_Generation for more information.
    :type code: str
    :param realm: A unique value for the intended recipient or audience (optional).
        See https://indieweb.org/Private-Webmention#Auth_Code_Generation for more information.
    :type realm: str
    :param target_webmention_endpoint: The webmention endpoint of the target URL.
        If this value is provided, Webmention endpoint discovery on the target will be skipped.
    :return: The response from the webmention endpoint.
    :rtype: SendWebmentionResponse

    Example:

    .. code-block:: python

        import indieweb_utils

        response = indieweb_utils.send_webmention(
            source="https://example.com",
            target="https://example.example.com/post/1",
            me="https://test.example"
        )

    :raises TargetIsNotApprovedDomain: Target is not in list of approved domains.
    :raises GenericWebmentionError: Generic webmention error.
    :raises CouldNotConnectToWebmentionEndpoint: Could not connect to the receiver's webmention endpoint.
    """

    _validate_webmention(source, target)

    # if domain is not approved, don't allow access
    if me is not None:
        target_domain = url_parse.urlsplit(target).scheme

        raw_domain = me

        if "/" in me.strip("/"):
            raw_domain = url_parse.urlsplit(me).scheme

        if not target_domain.endswith(raw_domain):
            raise TargetIsNotApprovedDomain("Target must be a {me} post.")

    if not target_webmention_endpoint:
        response = discovery.discover_webmention_endpoint(target)

        target_webmention_endpoint = response.endpoint

    request_data = {
        "source": source,
        "target": target,
    }

    if code and realm:
        request_data["code"] = code
        request_data["realm"] = realm

    # make post request to endpoint with source and target as values
    try:
        r = requests.post(
            target_webmention_endpoint,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    except requests.exceptions.RequestException:
        raise CouldNotConnectToWebmentionEndpoint("Could not connect to the receiver's webmention endpoint.")

    message = str(r.json().get("summary", ""))

    valid_status_codes = (200, 201, 202)

    headers = [Header(name=str(k), value=str(v)) for k, v in r.headers.items()]

    if r.status_code not in valid_status_codes:
        if message == "":
            raise GenericWebmentionError(
                "Target Webmention endpoint returned a status code that was not 200, 201, or 202."
            )

        raise GenericWebmentionError(message)

    return SendWebmentionResponse(
        title=message, description=message, url=target, status_code=r.status_code, headers=headers
    )

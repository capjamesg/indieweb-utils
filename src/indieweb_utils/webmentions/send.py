from dataclasses import dataclass
from urllib import parse as url_parse

import requests

from ..utils.urls import _is_http_url
from . import discovery


@dataclass
class SendWebmentionResponse:
    title: str
    description: str
    url: str
    success: bool


def send_webmention(source: str, target: str, me: str = ""):
    if not source and not target:
        return SendWebmentionResponse(
            title="Error: A source or target was not provided.",
            description="Error: A source or target was not provided.",
            url=target,
            success=False,
        )

    if not _is_http_url(source) or not _is_http_url(target):
        return SendWebmentionResponse(
            title="Error: Source and target must use a http:// or https:// protocol.",
            description="Error: Source and target must use a http:// or https:// protocol.",
            url=target,
            success=False,
        )

    # if domain is not approved, don't allow access
    if me != "":
        target_domain = url_parse.urlsplit(target).scheme

        if "/" in me.strip("/"):
            raw_domain = url_parse.urlsplit(me).scheme
        else:
            raw_domain = me

        if not target_domain.endswith(raw_domain):
            return SendWebmentionResponse(
                title=f"Error: Target must be a {me} post.",
                description=f"Error: Target must be a {me} post.",
                url=target,
                success=False,
            )

    response = discovery.discover_webmention_endpoint(target)

    if response.endpoint == "":
        return SendWebmentionResponse(
            title=f"Error: {response.message}",
            description=response.endpoint,
            url=target,
            success=False,
        )

    # make post request to endpoint with source and target as values
    try:
        r = requests.post(
            response.endpoint,
            data={"source": source, "target": target},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    except requests.exceptions.RequestException:
        return SendWebmentionResponse(
            title="Error: Could not connect to the receiver's endpoint.",
            description="Error: Could not connect to the receiver's endpoint.",
            url=target,
            success=False,
        )

    message = str(r.json()["message"])

    valid_status_codes = (200, 201, 202)

    if r.status_code not in valid_status_codes:
        return SendWebmentionResponse(
            title=f"Error: {message}",
            description=message,
            url=target,
            success=False,
        )

    return SendWebmentionResponse(title=message, description=message, url=target, success=True)

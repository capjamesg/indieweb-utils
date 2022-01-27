import requests

from dataclasses import dataclass
from urllib import parse as url_parse

import requests

from . import discovery

@dataclass
class SendWebmentionResponse:
    title: str
    description: str
    url: str
    status: bool

def send_webmention(source: str, target: str, me: str = ""):
    if not source and not target:
        return SendWebmentionResponse(
            title=f"Error: A source or target was not provided.",
            description=f"Error: A source or target was not provided.",
            url=target,
            success=False,
        )

    if not target.startswith("https://") or not target.startswith("http://"):
        return SendWebmentionResponse(
            title=f"Error: Target must use a http:// or https:// protocol.",
            description=f"Error: Target must use a http:// or https:// protocol.",
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

    endpoint, message = discovery.discover_webmention_endpoint(target)

    if endpoint is None:
        return SendWebmentionResponse(
            title=f"Error: {message}",
            description=message,
            url=target,
            success=False,
        )

    # make post request to endpoint with source and target as values
    r = requests.post(
        endpoint,
        data={"source": source, "target": target},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
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

    return SendWebmentionResponse(
        title=message,
        description=message,
        url=target,
        success=True
    )
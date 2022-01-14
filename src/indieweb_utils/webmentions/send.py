import requests
from urllib import parse as url_parse

from . import discovery


def send_webmention(source, target, me=None):
    if not source and not target:
        message = {
            "title": "Please enter a source and target.",
            "description": "Please enter a source and target.",
            "url": target,
            "status": "failed",
        }

        return message

    if not target.startswith("https://"):
        message = {
            "title": "Error: Target must use https:// protocol.",
            "description": "Target must use https:// protocol.",
            "url": target,
            "status": "failed",
        }

        return message

    # if domain is not approved, don't allow access
    if me is not None:
        target_domain = url_parse.urlsplit(target).scheme

        if "/" in me.strip("/"):
            raw_domain = url_parse.urlsplit(me).scheme
        else:
            raw_domain = me

        if not target_domain.endswith(raw_domain):
            message = {
                "title": f"Error: Target must be a {me} post.",
                "description": f"Target must be a {me} post.",
                "url": target,
                "status": "failed",
            }

            return message

    endpoint, message = discovery.discover_webmention_endpoint(target)

    if endpoint is None:
        message = {"title": "Error:" + message, "description": message, "url": target, "status": "failed"}

        return message

    # make post request to endpoint with source and target as values
    r = requests.post(
        endpoint,
        data={"source": source, "target": target},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    message = str(r.json()["message"])

    valid_status_codes = (200, 201, 202)

    if r.status_code in valid_status_codes:
        message = {"title": message, "description": message, "url": target, "status": "success"}
    else:
        message = {"title": "Error: " + message, "description": "Error: " + message, "url": target, "status": "failed"}

    return message

import requests


def subscribe(hub: str, topic: str, callback: str) -> None:
    """
    Subscribe to changes to a URL.

    :param hub: The URL of the WebSub hub to inform.
    :param topic: The URL of the topic to subscribe to.
    :param callback: The URL of the callback that will be informed of changes.

    :returns: The response from the hub.

    :raises Exception: If the hub returns a non-202 status code.
    """
    resp = requests.post(
        hub,
        data={
            "hub.mode": "subscribe",
            "hub.topic": topic,
            "hub.callback": callback,
        },
    )

    if resp.status_code != 202:
        raise Exception(f"Failed to publish content to {hub} (status code returned was {resp.status_code})")


def unsubscribe(hub: str, topic: str, callback: str) -> None:
    """
    Unsubscribe from changes to a URL.

    :param hub: The URL of the WebSub hub to inform.
    :param topic: The URL of the topic to unsubscribe from.

    :returns: The response from the hub.

    :raises Exception: If the hub returns a non-202 status code.
    """
    resp = requests.post(
        hub,
        data={
            "hub.mode": "unsubscribe",
            "hub.topic": topic,
            "hub.callback": callback,
        },
    )

    if resp.status_code != 202:
        raise Exception(f"Failed to publish content to {hub} (status code returned was {resp.status_code})")

    return resp


def publish(hub: str, topic: str) -> None:
    """
    Inform a hub that a topic has changed.

    :param hub: The URL of the WebSub hub to inform.
    :param topic: The URL of the topic to publish changes to.

    :returns: The response from the hub.

    :raises Exception: If the hub returns a non-202 status code.
    """
    resp = requests.post(
        hub,
        data={
            "hub.mode": "publish",
            "hub.topic": topic,
        },
    )

    if resp.status_code != 202:
        raise Exception(f"Failed to publish content to {hub} (status code returned was {resp.status_code})")

    return resp


def send_update_pings(source_url: str, hub_url: str, callback_urls: str, post_content: str = None, content_type: str = "application/text+html"):
    """
    Send an update ping to a list of URLs.

    Useful for implementing hub logic that will inform subscribers of updates.

    :param source_url: The URL of the source of the update.
    :param hub_url: The URL of your hub.
    :param callback_urls: A list of URLs to inform of the update.
    :param post_content: The content to send in the POST request. This should be equal to the content of the source URL.

    :returns: A list of responses from the target URLs.
    """
    responses = []

    if post_content is None:
        resp = requests.get(source_url)
        post_content = resp.content

    for target_url in callback_urls:
        resp = requests.post(
            target_url,
            headers={
                "Link": f'<{source_url}>; rel="self", <{hub_url}>; rel="hub"',
                "Content-Type": content_type,
            },
            data=post_content,
        )

        responses.append(resp)

    return responses

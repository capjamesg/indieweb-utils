from typing import List

import mf2py


def get_reply_urls(url: str, html: str = None) -> List[str]:
    """
    Retrieve a list of all of the URLs to which a given post is responding using a u-in-reply-to microformat.

    :refs: https://indieweb.org/in-reply-to#How_to_consume_in-reply-to

    :param url: The URL to get replies to.
    :type url: str
    :param html: The HTML of the page whose replies you want to retrieve.
    :type html: str
    :return: A list of all of the URLs to which the given post responds.
    :rtype: list

    Example:

    .. code-block:: python

        import indieweb_utils

        reply_urls = indieweb_utils.get_reply_urls("https://aaronparecki.com/2022/10/10/17/")

        print(reply_urls) # ["https://twitter.com/amandaljudkins/status/1579680989135384576?s=12"]
    """

    if html:
        parsed_document = mf2py.parse(doc=html)
    else:
        parsed_document = mf2py.parse(url=url)

    in_reply_to_urls = []

    for item in parsed_document["items"]:
        if item["type"][0] != "h-entry":
            continue

        if item["properties"].get("in-reply-to") is None:
            continue

        for reply_item in item["properties"]["in-reply-to"]:
            url_list = reply_item["properties"].get("url")

            if url_list is None:
                continue

            in_reply_to_urls.extend(url_list)

    # only return unique urls
    return list(set(in_reply_to_urls))

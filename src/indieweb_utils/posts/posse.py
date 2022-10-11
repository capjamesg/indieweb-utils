from typing import List

import mf2py


def get_syndicated_copies(url: str, html: str = None) -> List[str]:
    """
    Retrieve the URLs for syndicated copies of a post.

    :refs: https://indieweb.org/discovery-algorithms#POSSE_copies

    :param url: The URL of the post whose syndicated copies you want to retrieve.
    :type url: str
    :param html: The HTML of the post whose syndicated copies you want to retrieve.
    :type html: str
    :return: A list of URLs for syndicated copies of the post.
    :rtype list

    Example:

    .. code-block:: python

        import indieweb_utils

        syndicate_copies = indieweb_utils.get_syndicated_copies("https://aaronparecki.com/2022/09/26/18/eyefi")

        for url in syndicate_copies:
            print(url)
    """

    if html:
        parsed_web_page = mf2py.parse(doc=html)
    else:
        parsed_web_page = mf2py.parse(url=url)

    syndication_urls = []

    for item in parsed_web_page["items"]:
        if item["type"][0] != "h-entry":
            continue

        properties = item["properties"]

        if properties.get("syndication") is None:
            continue

        for url in properties["syndication"]:
            syndication_urls.append(url)

    return syndication_urls

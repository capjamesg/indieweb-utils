import dataclasses
from typing import Any, Dict, List, Tuple

import mf2py

from ..webmentions import send_webmention


@dataclasses.dataclass
class SalmentionParsedResponse:
    NewResponses: List[dict]
    Webmentions: Dict[str, Any]
    DeletedPosts: List[dict]


SUPPORTED_TYPES = [
    "h-entry",
]

EXPANDED_SUPPORTED_TYPES = [
    "h-review",
    "h-event",
    "h-recipe",
    "h-resume",
    "h-product",
    "h-cite",
]


def _check_supported_type(parsed_mf2_tree: dict, supported_types: list) -> bool:
    """
    Check if the parsed mf2 tree contains a supported type.

    :param parsed_mf2_tree: The parsed mf2 tree.
    :type parsed_mf2_tree: dict
    :param supported_types: The supported types.
    :type supported_types: list
    :returns: True if the parsed mf2 tree contains a supported type, False otherwise.
    :rtype: bool
    """
    if parsed_mf2_tree.get("type", [])[0] in supported_types:
        return True

    return False


def _get_nested_h_entry(parsed_mf2_tree: dict, supported_types: list) -> List[dict]:
    """
    Get the nested h-* objects from a parsed mf2 tree.

    :param parsed_mf2_tree: The parsed mf2 tree.
    :type parsed_mf2_tree: dict
    :param supported_types: The supported types.
    :type supported_types: list
    :returns: The nested h-* objects.
    :rtype: dict
    """

    entries = []

    for entry in parsed_mf2_tree.get("items", []):
        if _check_supported_type(entry, supported_types):
            entries.append(entry)

        if entry.get("type") == ["h-feed"]:
            entries.append(_get_nested_h_entry(entry.get("children"), supported_types))

    return entries


def process_salmention(
    current_page_contents: str,
    original_post_contents: str,
    page_url: str,
    supported_types: list = SUPPORTED_TYPES,
    send_upstream_webmentions: bool = True,
) -> Tuple[List[dict], List[str], List[str]]:
    """
    Process a Salmention. Call this function only when you receive a Webmention
    to a page that has already received a Webmention.

    :param url: The URL of the page that received the Webmention.
    :type url: str
    :param original_post_contents: The HTML contents of the original post.
    :type original_post_contents: str
    :param current_page_contents: The HTML contents of the current page.
    :type current_page_contents: str
    :returns: The new nested responses, the URLs of the webmentions sent, and the URLs of the deleted posts.
    :rtype: Tuple[List[dict], List[str], List[str]]

    Example:

    .. code-block:: python

        from indieweb_utils import process_salmention

        process_salmention('<html>...</html>', '<html>...</html>')
    """

    new_parsed_mf2_tree = mf2py.parse(current_page_contents)
    new_nested_entry = _get_nested_h_entry(new_parsed_mf2_tree, supported_types)

    original_parsed_mf2_tree = mf2py.parse(original_post_contents)
    original_nested_entry = _get_nested_h_entry(original_parsed_mf2_tree, supported_types)

    # return new nested responses
    new_nested_responses = []

    all_original_urls = [x["properties"].get("url", [])[0] for x in original_nested_entry]

    all_new_urls = [x["properties"].get("url", [])[0] for x in new_nested_entry]

    deleted_posts = [x for x in all_new_urls if x not in all_original_urls]

    urls_in_both = [x for x in all_new_urls if x in all_original_urls]

    # remove empty items
    deleted_posts = [x for x in deleted_posts if x]

    if not original_nested_entry:
        return new_nested_responses, [], deleted_posts

    urls_webmentions_sent = {"success": [], "failed": []}

    # for all nested urls, send webmentions
    for response in original_nested_entry:
        if response["properties"]["url"][0] not in all_new_urls:
            new_nested_responses.append(response)

    for url in urls_in_both:
        if url == page_url or send_upstream_webmentions == False:
            continue

        try:
            send_webmention(url, page_url)
            urls_webmentions_sent["success"].append(url)
        except Exception as e:
            urls_webmentions_sent["failed"].append(url)

    return SalmentionParsedResponse(new_nested_responses, urls_webmentions_sent, deleted_posts)
    # 1. Send Webmention from /salmention/3 to /salmention/2/
    # 2. Send Webmention to /salmention/1/ telling it that /salmention/2/ has been updated
    # 3. /salmention/1/ compares old /salmention/2/ with new /salmention/2/
    # 4. /salmention/1/ shows all new responses inline
    # 5. Send Webmentions to all posts that are the same

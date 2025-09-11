import re
from typing import Tuple, Optional, Dict

patterns = {
    r"https://(www\.)?reddit\.com/r/([^/]+)/?": r"https://www.reddit.com/r/\2.rss",
    r"https://(www\.)?pinterest\.com/([^/]+)/?": r"https://www.pinterest.com/\2.rss",
    r"https://(www\.)?github\.com/([^/]+)/?": r"https://github.com/\2.atom",
    r"https:\/\/?(www\.|medium\.com\/)(@.*)": r"https://medium.com/feed/\2",
    r"https:\/\/?(www\.|[^\/]+\.tumblr\.com)\/?": r"https://\2.tumblr.com/rss",
    r"https:\/\/?(www\.|arxiv\.org\/list\/)([^\/]+)\/recent": r"https://rss.arxiv.org/rss/\2",
}

ACTIVITYPUB_USERNAME_REGEX = re.compile(r"^@([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)$")
BLUESKY_USERNAME_REGEX = re.compile(r"^@([a-zA-Z0-9._-]+)")


def get_web_feed_url(url: str) -> Optional[Tuple[str, str]]:
    """
    Given a URL, return the corresponding feed URL if it matches a known pattern.

    :param url: The URL to check.
    :type url: str
    :return: A tuple containing the feed URL and an empty string, or (None,
                None) if no pattern matches.
    """
    for pattern, feed in patterns.items():
        if re.match(pattern, url):
            result = re.sub(pattern, feed, url)
            return result, ""
    return None, None


def check_if_feed_is_activitypub(url: str) -> Optional[str]:
    """
    Check if a URL is likely an ActivityPub profile URL, based on the pattern "https://example.com/@username".

    :param url: The URL to check.
    :type url: str
    :return: The ActivityPub handle in the format "@username@domain" if it matches the pattern, otherwise False.
    :rtype: str | None
    """
    # if matches @x@y.com, return
    if re.match(r"^@.*@.*\..*$", url):
        return url
    result = re.match(r"https:\/\/(www\.)?(?!instagram|x.com|twitter.com|facebook.com)([^\/]+)\/@(.*)", url)
    if result:
        return f"@{result.group(3)}@{result.group(2)}"
    return None


def check_if_feed_is_bsky(url: str) -> Optional[str]:
    """
    Check if a URL is likely a Bluesky profile URL, based on the pattern "https://bsky.app/profile/username".

    :param url: The URL to check.
    :type url: str
    :return: The Bluesky handle in the format "@username" if it matches the pattern, otherwise None.
    :rtype: str | None
    """

    result = re.match(r"https:\/\/?(www\.|bsky\.app\/profile\/)([^\/]+)", url)
    if result:
        return f"@{result.group(2)}"
    return None

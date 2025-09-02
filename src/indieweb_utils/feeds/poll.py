import requests
from granary import atom, jsonfeed, microformats2, rss

from ..constants import USER_AGENT

class FailedToFetchFeed(Exception):
    pass


class UnsupportedFeedFormat(Exception):
    pass


def retrieve_feed_contents(feed, format="jsonfeed"):
    """
    Retrieve the contents from a feed.

    This function returns contents as a JSON Feed.

    :param feed: The URL of the feed.
    :type feed: str
    :param format: The format to return the feed in.
    :type format: str
    :return: The contents of the feed.
    :rtype: dict

    Example:

    .. code-block:: python

        import indieweb_utils

        feed = "https://jamesg.blog/feeds/posts.xml"

        feed_contents = indieweb_utils.retrieve_feed_contents(feed)

        print(feed_contents)
    """
    FEED_IDENTIFICATION = {
        "rss+xml": rss.to_activities,
        "atom+xml": atom.atom_to_activities,
        "html": microformats2.html_to_activities,
        "feed+json": jsonfeed.jsonfeed_to_activities,
        "json": jsonfeed.jsonfeed_to_activities,
        "mf2+json": microformats2.json_to_activities,
    }

    if format == "jsonfeed":
        CONVERSION_FUNCTION = jsonfeed.activities_to_jsonfeed
    else:
        raise ValueError("Unsupported format")

    try:
        resp = requests.get(feed, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
    except requests.RequestException:
        raise FailedToFetchFeed("Request to retrieve feed did not return a valid response.")

    if resp.status_code != 200:
        raise FailedToFetchFeed("Request to retrieve feed did not return a valid response.")

    content_type = resp.headers.get("Content-Type", "").split(";")[0].split("/")[1]

    if content_type not in FEED_IDENTIFICATION:
        raise UnsupportedFeedFormat("Feed format is not supported, according to feed Content-Type header.")

    if content_type in ["json", "feed+json"]:
        activities = CONVERSION_FUNCTION(FEED_IDENTIFICATION[content_type](resp.json())[0])
    else:
        activities = CONVERSION_FUNCTION(FEED_IDENTIFICATION[content_type](resp.text))

    return activities

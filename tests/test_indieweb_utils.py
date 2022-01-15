# Partial test coverage is implemented for various functions in the library
# Assistance is requested to achieve full test coverage
import mf2py
import pytest

from indieweb_utils import *


class TestWebPageFeedDiscovery:
    def test_webpage_feed_discovery(self):
        feeds = discover_web_page_feeds("https://jamesg.blog/")

        assumed_feeds = [
            "https://jamesg.blog/",  # h-feed
            "https://jamesg.blog/feeds/posts.xml",
            "https://jamesg.blog/feeds/posts.jf2",
            "https://jamesg.blog/feeds/posts.json",
        ]

        for f in feeds:
            assert f.url in assumed_feeds

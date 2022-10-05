import pytest
import responses


class TestWebPageFeedDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import discover_web_page_feeds

        return discover_web_page_feeds

    @responses.activate
    def test_webpage_feed_discovery(self, target, index, index_url):
        responses.add(responses.Response(method="GET", url=index_url, body=index))

        actual_feeds = target(index_url)

        expected_feeds = {
            "https://jamesg.blog/",  # h-feed
            "https://jamesg.blog/feeds/posts.xml",
            "https://jamesg.blog/feeds/posts.jf2",
            "https://jamesg.blog/feeds/posts.json",
        }

        for feed in actual_feeds:
            assert feed.url in expected_feeds

    @responses.activate
    def test_webpage_feed_discovery_2(self, target, index2, index_url):
        responses.add(responses.Response(method="GET", url=index_url, body=index2))

        actual_feeds = target(index_url)

        expected_feeds = {"https://jamesvandyne.com/feed/"}

        for feed in actual_feeds:
            assert feed.url in expected_feeds

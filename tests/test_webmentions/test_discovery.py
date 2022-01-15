import pytest
import responses


class TestWebmentionEndpointDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import discover_webmention_endpoint

        return discover_webmention_endpoint

    @responses.activate
    def test_webmention_endpoint_discovery(self, target, article, article_url):
        responses.add(responses.Response(method="GET", url=article_url, body=article))
        endpoints = target(article_url)
        assert len(endpoints) > 0
        assert endpoints[0] == "https://webmention.jamesg.blog/endpoint"

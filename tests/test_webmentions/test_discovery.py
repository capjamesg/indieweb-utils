import pytest
import responses


class TestWebmentionEndpointDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import discover_webmention_endpoint

        return discover_webmention_endpoint

    @responses.activate
    def test_webmention_searches_html(self, target, article, article_url):
        responses.add(responses.Response(method="GET", url=article_url, body=article))
        get_endpoint = target(article_url)

        assert get_endpoint.endpoint == "https://webmention.jamesg.blog/endpoint"

    @responses.activate
    def test_webmention_searches_header(self, target, article_url):
        responses.add(
            responses.Response(
                method="GET",
                url=article_url,
                body="",
                headers={
                    "link": (
                        "<https://webmention.jamesg.blog/endpoint>; rel='webmention',"
                        "<https://auth.jamesg.blog/auth>; rel='authorization_endpoint'"
                    )
                },
            )
        )
        get_endpoint = target(article_url)

        assert get_endpoint.endpoint == "https://webmention.jamesg.blog/endpoint"

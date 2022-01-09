# Partial test coverage is implemented for various functions in the library
# Assistance is requested to achieve full test coverage
import pytest

from indieweb_utils import *


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://www.example.com/", "http://www.example.com/"),
        ("example.com/", "https://example.com/"),
        ("http://www.example.com:80/", "http://www.example.com/"),
        ("example.com/../", "https://example.com/"),
        ("example.com/./image.png", "https://example.com/image.png"),
        ("example.com/../image.png", "https://example.com/image.png"),
    ],
)
def test_canonicalize_url(url, expected):
    domain = "example.com"
    assert canonicalize_url(url=url, domain=domain) == expected


class TestWebmentionEndpointDiscovery:
    def test_webmention_endpoint_discovery(self):
        # TODO: Mock the request so unit tests are making network requests
        endpoints = discover_webmention_endpoint("https://jamesg.blog/2021/12/06/advent-of-bloggers-6/")
        assert len(endpoints) > 0
        assert endpoints[0] == "https://webmention.jamesg.blog/endpoint"


class TestPostTypeDiscovery:
    def test_post_type_discovery(self):
        # TODO: Mock the request so unit tests are making network requests
        post_url = "https://jamesg.blog/2021/12/06/advent-of-bloggers-6/"

        parsed = mf2py.parse(url=post_url)

        h_entry = [item for item in parsed["items"] if item.get("type") == ["h-entry"]]

        assert get_post_type(h_entry[0]) == "article"

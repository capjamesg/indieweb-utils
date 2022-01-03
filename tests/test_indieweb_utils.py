# Partial test coverage is implemented for various functions in the library
# Assistance is requested to achieve full test coverage

from indieweb_utils import *
import mf2py


class TestCanonicalizeURL:
    def test_canonicalize_url(self):
        assert canonicalize_url('http://www.example.com/', "example.com") == 'http://www.example.com/'
        assert canonicalize_url('example.com/', "example.com") == 'https://example.com/'
        assert canonicalize_url('http://www.example.com:80/', "example.com") == 'http://www.example.com/'
        assert canonicalize_url('example.com/../', "example.com") == 'https://example.com/'
        assert canonicalize_url('example.com/./image.png', "example.com") == 'https://example.com/image.png'
        assert canonicalize_url('example.com/../image.png', "example.com") == 'https://example.com/image.png'


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

        h_entry = [item for item in parsed["items"] if item.get('type') == ['h-entry']]

        assert get_post_type(h_entry[0]) == "article"

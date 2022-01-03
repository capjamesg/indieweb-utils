# Partial test coverage is implemented for various functions in the library
# Assistance is requested to achieve full test coverage

from indieweb_utils import *
import unittest
import mf2py

class TestCanonicalizeURL(unittest.TestCase):
    def test_canonicalize_url(self):
        self.assertEqual(canonicalize_url('http://www.example.com/', "example.com"), 'http://www.example.com/')
        self.assertEqual(canonicalize_url('example.com/', "example.com"), 'https://example.com/')
        self.assertEqual(canonicalize_url('http://www.example.com:80/', "example.com"), 'http://www.example.com/')
        self.assertEqual(canonicalize_url('example.com/../', "example.com"), 'https://example.com/')
        self.assertEqual(canonicalize_url('example.com/./image.png', "example.com"), 'https://example.com/image.png')
        self.assertEqual(canonicalize_url('example.com/../image.png', "example.com"), 'https://example.com/image.png')

class TestWebmentionEndpointDiscovery(unittest.TestCase):
    def test_webmention_endpoint_discovery(self):
        self.assertEqual(discover_webmention_endpoint("https://jamesg.blog/2021/12/06/advent-of-bloggers-6/")[0], "https://webmention.jamesg.blog/endpoint")

class TestPostTypeDiscovery(unittest.TestCase):
    def test_post_type_discovery(self):
        post_url = "https://jamesg.blog/2021/12/06/advent-of-bloggers-6/"

        parsed = mf2py.parse(url=post_url)

        h_entry = [item for item in parsed["items"] if item.get('type') == ['h-entry']]

        if h_entry:
            self.assertEqual(get_post_type(h_entry[0]), "article")
        else:
            return True

if __name__ == "__main__":
    unittest.main()
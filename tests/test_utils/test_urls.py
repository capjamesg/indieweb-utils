import pytest

from indieweb_utils import utils


@pytest.mark.parametrize(
    "url, domain, expected",
    [
        ("http://www.example.com/", "www.example.com", "http://www.example.com/"),
        ("example.com/", "example.com", "https://example.com/"),
        ("http://www.example.com:80/", "www.example.com", "http://www.example.com/"),
        ("example.com/../", "example.com", "https://example.com/"),
        ("example.com/./image.png", "example.com", "https://example.com/image.png"),
        ("example.com/../image.png", "example.com", "https://example.com/image.png"),
    ],
)
def test_canonicalize_url(url, domain, expected):
    assert utils.canonicalize_url(url=url, domain=domain) == expected

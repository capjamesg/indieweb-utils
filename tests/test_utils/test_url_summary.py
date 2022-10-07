import pytest

from indieweb_utils import utils


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/capjamesg/indieweb-utils/issues/58",
            "A comment on issue #58 in the indieweb-utils GitHub repository",
        ),
        (
            "https://github.com/capjamesg/indieweb-utils/pull/62",
            "A comment on pull request #62 in the indieweb-utils GitHub repository",
        ),
        (
            "https://www.github.com/capjamesg/indieweb-utils",
            "A comment on the indieweb-utils GitHub repository",
        ),
        (
            "https://github.com/capjamesg/indieweb-utils",
            "A comment on the indieweb-utils GitHub repository",
        ),
        (
            "https://eventbrite.co.uk/e/prewired-registration-15338031465",
            "An event on Eventbrite",
        ),
        (
            "https://events.indieweb.org/2022/10/homebrew-website-club-europe-london-AInXEh6WBbqn",
            "An event on IndieWeb events",
        ),
        (
            "https://twitter.com/jack/status/20",
            "A tweet by @jack",
        ),
        ("https://jamesg.blog", "A post by jamesg.blog"),
        ("https://indieweb.org/coffee", "The /coffee page on the IndieWeb wiki"),
        ("https://www.indieweb.org/coffee", "The /coffee page on the IndieWeb wiki"),
        ("https://calagator.com/event", "An event on Calagator"),
        ("https://upcoming.com/event", "An event on Upcoming"),
    ],
)
def test_canonicalize_url(url, expected):
    assert utils.get_url_summary(url=url) == expected


def test_invalid_url():
    # make sure invalid URL raises an error
    with pytest.raises(utils.InvalidURL):
        utils.get_url_summary(url="jamesg")

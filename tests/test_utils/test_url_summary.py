import pytest

from indieweb_utils import utils


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://github.com/capjamesg/indieweb-utils/issues/58",
            "A comment on issue 58 in the indieweb-utils repository.",
        ),
        (
            "https://github.com/capjamesg/indieweb-utils/pull/62",
            "A comment on pull request 62 in the indieweb-utils repository.",
        ),
        (
            "https://github.com/capjamesg/indieweb-utils",
            "A comment on GitHub in the indieweb-utils repository.",
        ),
        (
            "https://www.eventbrite.co.uk/e/prewired-registration-15338031465",
            "An Eventbrite event.",
        ),
        (
            "https://events.indieweb.org/2022/10/homebrew-website-club-europe-london-AInXEh6WBbqn",
            "An IndieWeb event.",
        ),
        (
            "https://twitter.com/jack/status/20",
            "A Tweet from @jack.",
        ),
        ("https://jamesg.blog", "A post by jamesg.blog."),
    ],
)
def test_canonicalize_url(url, expected):
    assert utils.get_url_summary(url=url) == expected


def test_invalid_url():
    # make sure invalid URL raises an error
    with pytest.raises(utils.InvalidURL):
        utils.get_url_summary(url="jamesg")

import pytest
from indieweb_utils.utils import autolink_tags


@pytest.mark.parametrize(
    "text, tag_prefix, people, tags, expected",
    [
        (
            "I am drinking a cup of #coffee this cool #October.",
            "https://jamesg.blog/tag/",
            {},
            ["coffee", "October"],
            "I am drinking a cup of <a href='https://jamesg.blog/tag/coffee'>#coffee</a> this cool <a href='https://jamesg.blog/tag/October'>#October</a>.",  # noqa: E501
        ),
        (
            "I am drinking a cup of #coffee this cool #October. #awesome",
            "https://jamesg.blog/tag/",
            {},
            ["coffee", "october"],
            "I am drinking a cup of <a href='https://jamesg.blog/tag/coffee'>#coffee</a> this cool #October. #awesome",
        ),
        (
            "I am drinking a cup of #coffee this cool #October. #awesome",
            "https://jamesg.blog/tag/",
            {},
            ["coffee", "October"],
            "I am drinking a cup of <a href='https://jamesg.blog/tag/coffee'>#coffee</a> this cool <a href='https://jamesg.blog/tag/October'>#October</a>. #awesome",  # noqa: E501
        ),
        (
            "I am having lunch with @james.",
            "",
            {"james": ("James' Coffee Blog", "https://jamesg.blog")},
            [],
            "I am having lunch with <a href='https://jamesg.blog'>James' Coffee Blog</a>.",
        ),
        (
            "I am having #lunch with @james.",
            "https://jamesg.blog/tag/",
            {"james": ("James' Coffee Blog", "https://jamesg.blog")},
            ["lunch", "dinner"],
            "I am having <a href='https://jamesg.blog/tag/lunch'>#lunch</a> with <a href='https://jamesg.blog'>James' Coffee Blog</a>.",  # noqa: E501
        ),
        (
            "I am having #lunch with @james. #indieweb",
            "https://jamesg.blog/tag/",
            {"james": ("James' Coffee Blog", "https://jamesg.blog")},
            ["lunch", "indieweb"],
            "I am having <a href='https://jamesg.blog/tag/lunch'>#lunch</a> with <a href='https://jamesg.blog'>James' Coffee Blog</a>. <a href='https://jamesg.blog/tag/indieweb'>#indieweb</a>",  # noqa: E501
        ),
    ],
)
def test_canonicalize_url(text, tag_prefix, people, tags, expected):
    assert autolink_tags(text=text, tag_prefix=tag_prefix, people=people, tags=tags) == expected

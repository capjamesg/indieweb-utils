from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup

from ..parsing.parse import get_soup
from . import constants


class ProfileError(Exception):
    pass


@dataclass(frozen=True)
class Profile:
    name: str
    photo: Optional[str]
    url: str
    email: Optional[str]


def get_profile(me: str, html: str = "", soup: BeautifulSoup = None) -> Profile:
    """
    Return the profile information for the given me URL.

    :param me: The me URL to get the profile information for.
    :type me: str
    :return: The profile information.
    :rtype: Profile

    Get a profile from a url.

    :param me: The url to get the profile from.
    :type me: str
    :return: The profile.
    :rtype: Profile

    Example:

    .. code-block:: python

        import indieweb_utils

        me = "https://jamesg.blog"

        profile = indieweb_utils.get_profile(me)

        assert profile.email == "james@jamesg.blog"
        assert profile.name == "James"
        assert profile.photo == "https://jamesg.blog/me.jpg"
        assert profile.url == "https://jamesg.blog

    :raises ProfileError: Profile could not be retrieved.
    """

    if soup is None:
        profile_item = get_soup(html, me)
    else:
        profile_item = soup

    h_card_tag = profile_item.select(".h-card")

    try:
        h_card = h_card_tag[0]
    except IndexError:
        return Profile(name=me, photo=None, url=me, email=None)
    else:
        return Profile(
            name=_extract_name(h_card=h_card) or me,
            photo=_extract_photo(h_card=h_card),
            url=_extract_url(h_card=h_card) or me,
            email=_extract_email(h_card=h_card),
        )


def _extract_name(*, h_card) -> Optional[str]:
    name_tag = h_card.select(constants.HCardProfileSelector.name.value)
    try:
        name = name_tag[0]
    except IndexError:
        return None
    else:
        return name.text.strip()


def _extract_photo(*, h_card) -> Optional[str]:
    photo = h_card.select(constants.HCardProfileSelector.photo.value)
    try:
        return photo[0].get("src")
    except IndexError:
        return None


def _extract_url(*, h_card) -> Optional[str]:
    url_tag = h_card.select(constants.HCardProfileSelector.url.value)
    try:
        url = url_tag[0]
    except IndexError:
        return None
    else:
        return url.get("href").strip()


def _extract_email(*, h_card) -> Optional[str]:
    email_tag = h_card.select(constants.HCardProfileSelector.email.value)
    try:
        email = email_tag[0].get("href", "")
    except IndexError:
        return None
    else:
        return email.strip().replace("mailto:", "") or None

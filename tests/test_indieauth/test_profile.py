import pytest
import responses
from indieweb_utils.indieauth import profile


@pytest.fixture
def name_tag():
    return '<h1 class="p-name">John Doe</h1>'


@pytest.fixture
def photo_tag():
    return '<img src="http://example.com/me.jpg" class="u-photo"/>'


@pytest.fixture
def me_tag():
    return '<a href="http://example.com/john" class="u-url"></a>'


@pytest.fixture
def email_tag():
    return '<a href="mailto:john@example.com" class="u-email"></a>'


@responses.activate
def test_parses_profile(name_tag, photo_tag, me_tag, email_tag):
    """Test parsing a h-card."""
    url = "http://example.com"

    body = f'<div class="h-card">{name_tag}{photo_tag}{me_tag}{email_tag}</div>'

    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body=body,
        )
    )
    actual = profile.get_profile(url, html=body)

    assert actual.name == "John Doe"
    assert actual.photo == "http://example.com/me.jpg"
    assert actual.url == "http://example.com/john"
    assert actual.email == "john@example.com"


@responses.activate
def test_handles_missing_email(name_tag, photo_tag, me_tag):
    """Test email is set to None if no email found."""
    url = "http://example.com"
    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body=f'<div class="h-card">{name_tag}{photo_tag}{me_tag}</div>',
        )
    )
    actual = profile.get_profile(me=url)
    assert actual.email is None


@responses.activate
def test_handles_missing_url(name_tag, photo_tag):
    """Should use me url for url if not found."""
    url = "http://example.com"
    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body=f'<div class="h-card">{name_tag}{photo_tag}</div>',
        )
    )
    actual = profile.get_profile(me=url)
    assert actual.url == url


@responses.activate
def test_handles_missing_photo(name_tag):
    """Tests for a None value returned for the 'photo' attribute if a photo is not found."""
    url = "http://example.com"
    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body=f'<div class="h-card">{name_tag}</div>',
        )
    )
    actual = profile.get_profile(me=url)
    assert actual.photo is None


@responses.activate
def test_handles_missing_name():
    """Test name is set to the me url if no name found."""
    url = "http://example.com"
    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body='<div class="h-card"></div>',
        )
    )
    actual = profile.get_profile(me=url)
    assert actual.name == url


@responses.activate
def test_handles_missing_h_card():
    """Tests that it returns a profile with the me url as the name if there is no h-card."""
    url = "http://example.com"
    responses.add(
        responses.Response(
            method="GET",
            url=url,
            body="",
        )
    )
    actual = profile.get_profile(me=url)
    assert actual.name == url
    assert actual.url == url
    assert actual.photo is None
    assert actual.email is None

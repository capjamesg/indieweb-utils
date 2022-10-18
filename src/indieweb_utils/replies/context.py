from dataclasses import dataclass
from typing import List, Tuple
from urllib import parse as url_parse

import mf2py
import requests
from bs4 import BeautifulSoup

from ..parsing.parse import get_soup
from ..utils.urls import _is_http_url, canonicalize_url
from ..webmentions.discovery import (
    LocalhostEndpointFound,
    TargetNotProvided,
    UnacceptableIPAddress,
    WebmentionEndpointNotFound,
    discover_webmention_endpoint,
)


@dataclass
class PostAuthor:
    """
    Information about the author of a post.
    """

    name: str
    url: str
    photo: str


@dataclass
class ReplyContext:
    """
    Context about a web page and its contents.
    """

    webmention_endpoint: str
    photo: str
    name: str
    video: str
    post_html: str
    post_text: str
    authors: List[PostAuthor]
    description: str


class ReplyContextRetrievalError(Exception):
    pass


class UnsupportedScheme(Exception):
    pass


def _get_author_properties(author_url: str, h_entry: dict) -> Tuple[str, str, str]:
    author_image = ""
    author_name = ""

    if h_entry["properties"].get("url"):
        author_url = h_entry["properties"]["url"][0]

    if h_entry["properties"].get("name"):
        author_name = h_entry["properties"]["name"][0]

    if h_entry["properties"].get("photo"):
        author_image = h_entry["properties"]["photo"][0]

    return author_url, author_name, author_image


def _process_h_entry_author(h_entry: dict, url: str, domain: str) -> Tuple[str, str, str]:
    parsed_url = url_parse.urlsplit(url)

    author_url = url
    author_image = ""
    author_name = ""

    if isinstance(h_entry["properties"]["author"][0], dict) and h_entry["properties"]["author"][0].get("type") == [
        "h-card"
    ]:
        h_card = h_entry["properties"]["author"][0]

        author_url, author_name, author_image = _get_author_properties(author_url, h_card)

    elif isinstance(h_entry["properties"]["author"][0], str):
        if h_entry["properties"]["author"][0].startswith("/"):
            author_url = parsed_url.scheme + "://" + domain + h_entry["properties"].get("author")[0]

        try:
            author = mf2py.parse(requests.get(author_url, timeout=10, verify=False).text)
        except requests.exceptions.RequestException:
            pass
        else:
            h_card = [item for item in author["items"] if item.get("type", []) == ["h-card"]][0]
            author_url, author_name, author_image = _get_author_properties(author_url, h_card)

    if author_url is not None and author_url.startswith("/"):
        author_url = parsed_url.scheme + "://" + domain + author_url

    if author_image is not None and author_image.startswith("/"):
        author_image = parsed_url.scheme + "://" + domain + author_image

    return author_url, author_image, author_name


def _process_post_contents(h_entry: dict, domain: str, author_image: str, summary_word_limit: int) -> Tuple[str, str]:
    if h_entry["properties"].get("content") and h_entry["properties"].get("content")[0].get("html"):
        post_body = h_entry["properties"]["content"][0]["html"]
        soup = BeautifulSoup(post_body, "html.parser")
        post_body = soup.text

        favicon = soup.find("link", rel="icon")

        if not favicon:
            favicon = soup.find("link", rel="shortcut icon")

        new_photo_url = ""

        if favicon:
            new_photo_url = _get_favicon(favicon["href"], domain)

        if not author_image and new_photo_url:
            author_image = new_photo_url

        post_body = " ".join(post_body.split(" ")[:summary_word_limit]) + " ..."
    elif h_entry["properties"].get("content"):
        post_body = h_entry["properties"]["content"]

        post_body = " ".join(post_body.split(" ")[:summary_word_limit]) + " ..."
    else:
        post_body = ""

    return author_image, post_body


def _generate_h_entry_reply_context(
    h_entry: dict,
    url: str,
    domain: str,
    webmention_endpoint_url: str,
    summary_word_limit: int,
) -> ReplyContext:
    p_name = ""
    post_body = ""
    author_image = ""
    author_name = ""
    author_url = ""

    if h_entry["properties"].get("author"):
        author_url, author_image, author_name = _process_h_entry_author(h_entry, url, domain)

    author_image, post_body = _process_post_contents(h_entry, domain, author_image, summary_word_limit)

    if h_entry["properties"].get("name"):
        p_name = h_entry["properties"]["name"][0]

    # get article name
    if h_entry["properties"].get("name"):
        p_name = h_entry["properties"]["name"][0]

    # use domain name as author name if no author name is found
    if not author_name and author_url:
        author_name = url_parse.urlsplit(author_url).netloc

    post_photo_url = ""
    post_video_url = ""
    summary = ""

    if h_entry["properties"].get("featured"):
        post_photo_url = canonicalize_url(h_entry["properties"]["featured"][0], domain, url)

    if h_entry["properties"].get("video"):
        post_video_url = canonicalize_url(h_entry["properties"]["video"][0], domain, url)

    # look for featured image to display in reply context
    if post_photo_url is None:
        post_photo_url = _get_featured_image(post_body, domain)

    if h_entry["properties"].get("summary"):
        summary = h_entry["properties"]["summary"][0]

        if isinstance(summary, dict):
            summary = summary["value"]
    else:
        summary = " ".join(". ".join(post_body.split(". ")[:2]).split(" ")[:summary_word_limit]) + "..."

    return ReplyContext(
        name=p_name,
        post_text=post_body,
        post_html=post_body,
        authors=[PostAuthor(url=author_url, name=author_name, photo=author_image)],
        photo=post_photo_url,
        video=post_video_url,
        webmention_endpoint=webmention_endpoint_url,
        description=summary,
    )


def _generate_tweet_reply_context(url: str, twitter_bearer_token: str, webmention_endpoint_url: str) -> ReplyContext:
    tweet_uid = url.strip("/").split("/")[-1]

    headers = {"Authorization": f"Bearer {twitter_bearer_token}"}

    try:
        r = requests.get(
            f"https://api.twitter.com/2/tweets/{tweet_uid}?tweet.fields=author_id",
            headers=headers,
            timeout=10,
            verify=False,
        )
    except requests.exceptions.RequestException:
        raise ReplyContextRetrievalError("Could not retrieve tweet context from the Twitter API.")

    if r and r.status_code != 200:
        raise ReplyContextRetrievalError(f"Twitter API returned {r.status_code}")

    base_url = f"https://api.twitter.com/2/users/{r.json()['data'].get('author_id')}"

    try:
        get_author = requests.get(
            f"{base_url}?user.fields=url,name,profile_image_url,username",
            headers=headers,
            timeout=10,
            verify=False,
        )
    except requests.exceptions.RequestException:
        raise ReplyContextRetrievalError("Could not retrieve tweet context from the Twitter API.")

    if get_author and get_author.status_code == 200:
        photo_url = get_author.json()["data"].get("profile_image_url")
        author_name = get_author.json()["data"].get("name")
        author_url = "https://twitter.com/" + get_author.json()["data"].get("username")
    else:
        photo_url = ""
        author_name = ""
        author_url = ""

    return ReplyContext(
        name=author_name,
        post_text=r.json()["data"].get("text"),
        post_html=r.json()["data"].get("html"),
        authors=[PostAuthor(url=author_url, name=author_name, photo=photo_url)],
        photo=photo_url,
        video="",
        webmention_endpoint=webmention_endpoint_url,
        description=r.json()["data"].get("text"),
    )


def _get_content_from_html_page(soup: BeautifulSoup, summary_word_limit: int) -> str:
    # get body tag
    main_tag = soup.find("body")

    if main_tag:
        p_tag = main_tag.find("h1")

        if p_tag:
            p_tag = p_tag.text
        else:
            p_tag = ""
    else:
        p_tag = ""

    if soup.select(".e-content"):
        p_tag = soup.select(".e-content")[0]

        # get first paragraph
        if p_tag:
            p_tag = p_tag.find("p")
            if p_tag:
                p_tag = p_tag.text

            p_tag = " ".join([w for w in p_tag.split(" ")[:summary_word_limit]]) + " ..."
        else:
            p_tag = ""

    return p_tag


def _get_featured_video(soup: BeautifulSoup, domain: str) -> str:
    video = soup.find("video")

    if video and video.get("src"):
        return canonicalize_url(video.get("src"), domain)

    return ""


def _get_featured_image(soup: BeautifulSoup, domain: str) -> str:
    post_photo_url = ""

    photo_selectors = (
        (".u-photo", "src"),
        ("meta[name='og:image']", "content"),
        ("meta[name='twitter:image:src']", "content"),
        ("meta[property='og:image']", "content"),
        ("meta[property='twitter:image:src']", "content"),
        (".logo", "src"),
    )

    for selector, attrib in photo_selectors:
        if not soup.select(selector):
            continue

        data = soup.select(selector)[0].get(attrib)

        if not data:
            continue

        post_photo_url = data
        break

    if post_photo_url != "":
        return canonicalize_url(post_photo_url, domain)

    return post_photo_url


def _get_favicon(photo_url: str, domain: str) -> str:
    if not _is_http_url(photo_url):
        photo_url = "https://" + domain + photo_url

    try:
        r = requests.get(photo_url, timeout=10, verify=False)

        if r.status_code != 200:
            photo_url = ""
    except requests.exceptions.RequestException:
        photo_url = ""

    return photo_url


def _generate_reply_context_from_main_page(
    url: str,
    http_headers: dict,
    domain: str,
    webmention_endpoint_url: str,
    summary_word_limit: int,
    html: str = "",
    soup: BeautifulSoup = None,
) -> ReplyContext:

    if soup is None:
        soup = get_soup(html, url, headers=http_headers)

    page_title = soup.find("title")

    meta_description = ""

    description_selectors = (
        "meta[name='description']",
        "meta[name='og:description']",
        "meta[name='twitter:description']",
        "meta[property='description']",
        "meta[property='og:description']",
        "meta[property='twitter:description']",
    )

    for selector in description_selectors:
        description = soup.select(selector)
        if description:
            meta_description = description[0]["content"]
            break

    if page_title:
        page_title = page_title.text

    p_tag = _get_content_from_html_page(soup, summary_word_limit)

    post_photo_url = _get_featured_image(soup, domain)

    video_url = _get_featured_video(soup, domain)

    favicon = soup.find("link", rel="icon")

    if not favicon:
        favicon = soup.find("link", rel="shortcut icon")

    photo_url = ""

    if favicon:
        photo_url = _get_favicon(favicon["href"], domain)

    if not _is_http_url(domain):
        author_url = "https://" + domain

    meta_description = meta_description.strip().replace("\n\n", " ").replace("\n", " ")

    return ReplyContext(
        name=page_title,
        post_text=p_tag,
        post_html=p_tag,
        authors=[PostAuthor(url=author_url, name="", photo=photo_url)],
        photo=post_photo_url,
        video=video_url,
        webmention_endpoint=webmention_endpoint_url,
        description=meta_description,
    )


def get_reply_context(url: str, twitter_bearer_token: str = "", summary_word_limit: int = 75) -> ReplyContext:
    """
    Generate reply context for use on your website based on a URL.

    :param url: The URL of the post to generate reply context for.
    :type url: str
    :param twitter_bearer_token: The optional Twitter bearer token to use.
        This token is used to retrieve a Tweet from Twitter's API if you want to generate context using a Twitter URL.
    :type twitter_bearer_token: str
    :param summary_word_limit: The maximum number of words to include in the summary (default 75).
    :type summary_word_limit: int
    :return: A ReplyContext object with information about the specified web page.
    :rtype: ReplyContext

    Example:

    .. code-block:: python

        import indieweb_utils

        context = indieweb_utils.get_reply_context(
            url="https://jamesg.blog",
            summary_word_limit=50
        )

        # print the name of the specified page to the console
        print(context.name) # "Home | James' Coffee Blog"

    :raises ReplyContextRetrievalError: Reply context cannot be retrieved.
    :raises UnsupportedScheme: The specified URL does not use http:// or https://.
    """

    parsed_url = url_parse.urlsplit(url)
    http_headers = {"Accept": "text/html", "User-Agent": "indieweb_utils"}

    if parsed_url.scheme not in ["http", "https"]:
        raise UnsupportedScheme(f"{parsed_url.scheme} is not supported.")

    try:
        page_content = requests.get(url, timeout=10, verify=False, headers=http_headers)
    except requests.exceptions.RequestException:
        raise ReplyContextRetrievalError("Could not retrieve page content.")

    if page_content.status_code != 200:
        raise ReplyContextRetrievalError(f"Page returned a {page_content.status_code} response.")

    try:
        webmention_endpoint_url_response = discover_webmention_endpoint(url)

        webmention_endpoint_url = webmention_endpoint_url_response.endpoint
    except (
        TargetNotProvided,
        WebmentionEndpointNotFound,
        UnacceptableIPAddress,
        LocalhostEndpointFound,
    ):
        webmention_endpoint_url = ""

    parsed = mf2py.parse(doc=page_content.text)

    domain = parsed_url.netloc

    if (
        parsed["items"]
        and parsed["items"][0]["type"] == ["h-entry"]
        and "name" in parsed["items"][0].get("properties", {})
    ):
        h_entry = parsed["items"][0]

        return _generate_h_entry_reply_context(h_entry, url, domain, webmention_endpoint_url, summary_word_limit)

    if parsed_url.netloc == "twitter.com" and twitter_bearer_token is not None:
        return _generate_tweet_reply_context(url, twitter_bearer_token, webmention_endpoint_url)

    return _generate_reply_context_from_main_page(
        url, http_headers, domain, webmention_endpoint_url, summary_word_limit
    )

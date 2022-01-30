from dataclasses import dataclass
from typing import List
from urllib import parse as url_parse

import mf2py
import requests
from bs4 import BeautifulSoup

from ..utils.urls import canonicalize_url
from ..webmentions.discovery import discover_webmention_endpoint


@dataclass
class PostAuthor:
    name: str
    url: str
    photo: str


@dataclass
class ReplyContext:
    webmention_endpoint: str
    post_url: str
    photo: str
    name: str
    video: str
    post_html: str
    post_text: str
    authors: List[PostAuthor]


class ReplyContextRetrievalError(Exception):
    def __init__(self, message):
        self.message = message


class UnsupportedScheme(Exception):
    def __init__(self, message):
        self.message = message


def _generate_h_entry_reply_context(
    h_entry: dict, url: str, domain: str, webmention_endpoint_url: str, summary_word_limit: int
) -> ReplyContext:
    author_url = ""
    author_name = ""
    author_image = ""

    p_name = ""
    post_body = ""

    parsed_url = url_parse.urlsplit(url)

    if h_entry["properties"].get("author"):
        if isinstance(h_entry["properties"]["author"][0], dict) and h_entry["properties"]["author"][0].get("type") == [
            "h-card"
        ]:
            if h_entry["properties"]["author"][0]["properties"].get("url"):
                author_url = h_entry["properties"]["author"][0]["properties"]["url"][0]
            else:
                author_url = url

            if h_entry["properties"]["author"][0]["properties"].get("name"):
                author_name = h_entry["properties"]["author"][0]["properties"]["name"][0]

            if h_entry["properties"]["author"][0]["properties"].get("photo"):
                author_image = h_entry["properties"]["author"][0]["properties"]["photo"][0]

        elif isinstance(h_entry["properties"]["author"][0], str):
            if h_entry["properties"].get("author") and h_entry["properties"]["author"][0].startswith("/"):
                author_url = parsed_url.scheme + "://" + domain + h_entry["properties"].get("author")[0]

            try:
                author = mf2py.parse(requests.get(author_url, timeout=10, verify=False).text)
            except requests.exceptions.RequestException:
                author = {}

            if author.get("items") and author["items"][0]["type"] == ["h-card"]:
                author_url = author["properties"]["author"][0]

                if author["items"][0]["properties"].get("name"):
                    author_name = author["properties"]["author"][0]["properties"]["name"][0]

                if author["items"]["properties"].get("photo"):
                    author_image = author["properties"]["author"][0]["properties"]["photo"][0]

        if author_url is not None and author_url.startswith("/"):
            author_url = parsed_url.scheme + "://" + domain + author_url

        if author_image is not None and author_image.startswith("/"):
            author_image = parsed_url.scheme + "://" + domain + author_image

    if h_entry["properties"].get("content") and h_entry["properties"].get("content")[0].get("html"):
        post_body = h_entry["properties"]["content"][0]["html"]
        soup = BeautifulSoup(post_body, "html.parser")
        post_body = soup.text

        favicon = soup.find("link", rel="icon")

        if favicon and not author_image:
            photo_url = favicon["href"]
            if not photo_url.startswith("https://") or not photo_url.startswith("http://"):
                author_image = "https://" + domain + photo_url

        post_body = " ".join(post_body.split(" ")[:summary_word_limit]) + " ..."
    elif h_entry["properties"].get("content"):
        post_body = h_entry["properties"]["content"]

        post_body = " ".join(post_body.split(" ")[:summary_word_limit]) + " ..."

    # get article name
    if h_entry["properties"].get("name"):
        p_name = h_entry["properties"]["name"][0]

    if author_url is not None and (not author_url.startswith("https://") and not author_url.startswith("http://")):
        author_url = "https://" + author_url

    if not author_name and author_url:
        author_name = url_parse.urlsplit(author_url).netloc

    post_photo_url = ""
    post_video_url = ""

    if h_entry["properties"].get("photo"):
        post_photo_url = canonicalize_url(h_entry["properties"]["photo"][0], domain, url)

    if h_entry["properties"].get("video"):
        post_video_url = canonicalize_url(h_entry["properties"]["video"][0], domain, url)

    # look for featured image to display in reply context
    if post_photo_url is None:
        meta_og_image = soup.find("meta", property="og:image")
        meta_twitter_image = soup.find("meta", property="twitter:image")

        if meta_og_image and meta_og_image.get("content"):
            post_photo_url = meta_og_image["content"]

        elif meta_twitter_image and meta_twitter_image.get("content"):
            post_photo_url = meta_twitter_image["content"]

    return ReplyContext(
        name=p_name,
        post_url=url,
        post_text=post_body,
        post_html=post_body,
        authors=[PostAuthor(url=author_url, name=author_name, photo=author_image)],
        photo=post_photo_url,
        video=post_video_url,
        webmention_endpoint=webmention_endpoint_url,
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
        raise Exception(f"Twitter API returned {r.status_code}")

    base_url = f"https://api.twitter.com/2/users/{r.json()['data'].get('author_id')}"

    get_author = requests.get(
        f"{base_url}?user.fields=url,name,profile_image_url,username", headers=headers, timeout=10, verify=False
    )

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
        post_url=url,
        post_text=r.json()["data"].get("text"),
        post_html=r.json()["data"].get("html"),
        authors=[PostAuthor(url=author_url, name=author_name, photo=photo_url)],
        photo=photo_url,
        video="",
        webmention_endpoint=webmention_endpoint_url,
    )


def _generate_reply_context_from_main_page(
    url: str, http_headers: dict, domain: str, webmention_endpoint_url: str, summary_word_limit: int
) -> ReplyContext:
    try:
        request = requests.get(url, headers=http_headers)
    except requests.exceptions.RequestException:
        raise ReplyContextRetrievalError("Could not retrieve the specified URL.")

    soup = BeautifulSoup(request.text, "lxml")

    page_title = soup.find("title")

    if page_title:
        page_title = page_title.text

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

    post_photo_url = ""

    # look for featured image to display in reply context
    if soup.select(".u-photo"):
        post_photo_url = soup.select(".u-photo")[0]["src"]
    elif soup.find("meta", property="og:image") and soup.find("meta", property="og:image")["content"]:
        post_photo_url = soup.find("meta", property="og:image")["content"]
    elif soup.find("meta", property="twitter:image") and soup.find("meta", property="twitter:image")["content"]:
        post_photo_url = soup.find("meta", property="twitter:image")["content"]

    favicon = soup.find("link", rel="icon")

    if favicon:
        photo_url = favicon["href"]
        if not photo_url.startswith("https://") and not photo_url.startswith("http://"):
            photo_url = "https://" + domain + photo_url

        try:
            r = requests.get(photo_url, timeout=10, verify=False)
        except requests.exceptions.RequestException:
            photo_url = ""

        if r.status_code != 200:
            photo_url = ""
    else:
        photo_url = ""

    if not domain.startswith("https://") and not domain.startswith("http://"):
        author_url = "https://" + domain

    return ReplyContext(
        name=page_title,
        post_url=url,
        post_text=p_tag,
        post_html=p_tag,
        authors=[PostAuthor(url=author_url, name="", photo=photo_url)],
        photo=post_photo_url,
        video="",
        webmention_endpoint=webmention_endpoint_url,
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
    :return: was successful (bool), reply context (dict) or error (dict), page accepts webmention (bool)
    :rtype: list
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

    webmention_endpoint_url_response = discover_webmention_endpoint(url)

    webmention_endpoint_url = webmention_endpoint_url_response.endpoint

    parsed = mf2py.parse(page_content.text)

    domain = parsed_url.netloc

    if parsed["items"] and parsed["items"][0]["type"] == ["h-entry"]:
        h_entry = parsed["items"][0]

        return _generate_h_entry_reply_context(
            h_entry, url, domain, webmention_endpoint_url, summary_word_limit
        )

    if parsed_url.netloc == "twitter.com" and twitter_bearer_token is not None:
        return _generate_tweet_reply_context(url, twitter_bearer_token, webmention_endpoint_url)

    return _generate_reply_context_from_main_page(
        url,
        http_headers,
        domain,
        webmention_endpoint_url,
        summary_word_limit
    )

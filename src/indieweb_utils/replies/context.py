from dataclasses import dataclass, asdict
from distutils.sysconfig import customize_compiler
from urllib import parse as url_parse
import mf2py
import requests
from bs4 import BeautifulSoup

from ..utils.urls import canonicalize_url
from ..webmentions.discovery import discover_webmention_endpoint


@dataclass
class ReplyContext:
    webmention_endpoint: str
    post_url: str
    photo: str
    name: str
    video: str
    post_html: str
    post_text: str
    author_name: str
    author_url: str
    author_photo: str


class ReplyContextRetrievalError(Exception):
    def __init__(self, message):
        self.message = message


def get_reply_context(url: str, twitter_bearer_token: bool = "") -> ReplyContext:
    """
    Generate reply context for use on your website based on a URL.

    :param url: The URL of the post to generate reply context for.
    :type url: str
    :param twitter_bearer_token: The optional Twitter bearer token to use. This token is used to retrieve a Tweet from Twitter's API if you want to generate context using a Twitter URL.
    :type twitter_bearer_token: str
    :return: was successful (bool), reply context (dict) or error (dict), page accepts webmention (bool)
    :rtype: list
    """

    return_object = ReplyContext
    photo_url = ""
    parsed_url = url_parse.urlsplit(url)
    http_headers = {"Accept": "text/html", "User-Agent": "indieweb_utils"}

    if not url.startswith("https://") and not url.startswith("http://"):
        return return_object

    try:
        page_content = requests.get(url, timeout=10, verify=False, headers=http_headers)
    except:
        raise ReplyContextRetrievalError("Could not retrieve page content.")

    if page_content.status_code != 200:
        raise ReplyContextRetrievalError("Page did not return a 200 response.")

    webmention_endpoint_url, _ = discover_webmention_endpoint(url)

    return_object.webmention_endpoint = webmention_endpoint_url

    parsed = mf2py.parse(page_content.text)

    domain = url.replace("https://", "").replace("http://", "").split("/")[0]

    if parsed["items"] and parsed["items"][0]["type"] == ["h-entry"]:
        h_entry = parsed["items"][0]

        author_url = ""
        author_name = ""
        author_image = ""

        if h_entry["properties"].get("author"):
            if type(h_entry["properties"]["author"][0]) == dict and h_entry["properties"]["author"][0].get(
                "type"
            ) == ["h-card"]:
                if h_entry["properties"]["author"][0]["properties"].get("url"):
                    author_url = h_entry["properties"]["author"][0]["properties"]["url"][0]
                else:
                    author_url = url

                if h_entry["properties"]["author"][0]["properties"].get("name"):
                    author_name = h_entry["properties"]["author"][0]["properties"]["name"][0]
                else:
                    author_name = ""

                if h_entry["properties"]["author"][0]["properties"].get("photo"):
                    author_image = h_entry["properties"]["author"][0]["properties"]["photo"][0]
                else:
                    author_image = ""
            elif type(h_entry["properties"]["author"][0]) == str:
                if h_entry["properties"].get("author") and h_entry["properties"]["author"][0].startswith("/"):
                    author_url = url.split("/")[0] + "//" + domain + h_entry["properties"].get("author")[0]

                author = mf2py.parse(requests.get(author_url, timeout=10, verify=False).text)

                if author["items"] and author["items"][0]["type"] == ["h-card"]:
                    author_url = h_entry["properties"]["author"][0]

                    if author["items"][0]["properties"].get("name"):
                        author_name = h_entry["properties"]["author"][0]["properties"]["name"][0]
                    else:
                        author_name = ""

                    if author["items"]["properties"].get("photo"):
                        author_image = h_entry["properties"]["author"][0]["properties"]["photo"][0]
                    else:
                        author_image = ""

            if author_url is not None and author_url.startswith("/"):
                author_url = url.split("/")[0] + "//" + domain + author_url

            if author_image is not None and author_image.startswith("/"):
                author_image = url.split("/")[0] + "//" + domain + author_image

        if h_entry["properties"].get("content") and h_entry["properties"].get("content")[0].get("html"):
            post_body = h_entry["properties"]["content"][0]["html"]
            soup = BeautifulSoup(post_body, "html.parser")
            post_body = soup.text

            favicon = soup.find("link", rel="icon")

            if favicon and not author_image:
                photo_url = favicon["href"]
                if not photo_url.startswith("https://") or not photo_url.startswith("http://"):
                    author_image = "https://" + domain + photo_url
            else:
                author_image = ""

            post_body = " ".join(post_body.split(" ")[:75]) + " ..."
        elif h_entry["properties"].get("content"):
            post_body = h_entry["properties"]["content"]

            post_body = " ".join(post_body.split(" ")[:75]) + " ..."
        else:
            post_body = ""

        # get p-name
        if h_entry["properties"].get("name"):
            p_name = h_entry["properties"]["name"][0]
        else:
            p_name = ""

        if author_url is not None and (
            not author_url.startswith("https://") and not author_url.startswith("http://")
        ):
            author_url = "https://" + author_url

        if not author_name and author_url:
            author_name = author_url.split("/")[2]

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

        return_object.name = p_name
        return_object.post_url = url
        return_object.post_text = post_body
        return_object.post_html = post_body
        return_object.author_url = author_url
        return_object.author_name = author_name
        return_object.author_photo = author_image

        if post_photo_url:
            return_object.photo = post_photo_url
        else:
            return_object.photo = ""

        if post_video_url:
            return_object.video = post_video_url
        else:
            return_object.video = ""

        return return_object

    elif parsed["items"] and parsed["items"][0]["type"] == ["h-card"]:
        h_card = parsed["items"][0]

        if h_card["properties"].get("name"):
            author_name = h_card["properties"]["name"][0]
        else:
            author_name = ""

        if h_card["properties"].get("photo"):
            author_image = h_card["properties"]["photo"][0]
            if author_image.startswith("//"):
                author_image = "https:" + author_image
            elif author_image.startswith("/"):
                author_image = url.split("/")[0] + "//" + domain + author_image
            elif author_image.startswith("http://") or author_image.startswith("https://"):
                author_image = author_image
            else:
                author_image = "https://" + domain + "/" + author_image
        else:
            author_image = ""

        if h_card["properties"].get("note"):
            post_body = h_card["properties"]["note"][0]
        else:
            post_body = ""

        return_object.name = ""
        return_object.post_url = url
        return_object.post_text = post_body
        return_object.post_html = post_body
        return_object.author_url = url
        return_object.author_name = author_name
        return_object.author_photo = author_image
        return_object.photo = ""
        return_object.video = ""

        return return_object

    h_entry = {}

    if parsed_url.netloc == "twitter.com" and twitter_bearer_token is not None:
        
        tweet_uid = url.strip("/").split("/")[-1]

        headers = {"Authorization": f"Bearer {twitter_bearer_token}"}

        r = requests.get(
            f"https://api.twitter.com/2/tweets/{tweet_uid}?tweet.fields=author_id",
            headers=headers,
            timeout=10,
            verify=False,
        )

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

        return_object.name = ""
        return_object.post_url = url
        return_object.post_text = r.json()["data"].get("text")
        return_object.post_html = r.json()["data"].get("html")
        return_object.author_url = author_url
        return_object.author_name = author_name
        return_object.author_photo = photo_url
        return_object.photo = ""
        return_object.video = ""

        # convert type class to dictionary
        h_entry = asdict(h_entry)

        return h_entry

    request = requests.get(url, headers=http_headers)

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

            p_tag = " ".join([w for w in p_tag.split(" ")[:75]]) + " ..."
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

    if favicon and not photo_url:
        photo_url = favicon["href"]
        if not photo_url.startswith("https://") and not photo_url.startswith("http://"):
            photo_url = "https://" + domain + photo_url

        r = requests.get(photo_url, timeout=10, verify=False)

        if r.status_code != 200:
            photo_url = ""
    else:
        photo_url = ""

    if not domain.startswith("https://") and not domain.startswith("http://"):
        author_url = "https://" + domain

    return_object.name = ""
    return_object.post_url = url
    return_object.post_text = p_tag
    return_object.post_html = p_tag
    return_object.author_url = author_url
    return_object.author_name = ""
    return_object.author_photo = photo_url

    if post_photo_url:
        return_object.photo = post_photo_url
    else:
        return_object.photo = ""

    return_object.video = ""

    return h_entry

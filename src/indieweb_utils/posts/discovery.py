import re

import mf2py
import requests
from bs4 import BeautifulSoup


def discover_original_post(posse_permalink: str):
    """
    Find the original version of a post per the Original Post Discovery algorithm.

    refs: https://indieweb.org/original-post-discovery#Algorithm

    :param posse_permalink: The permalink of the post.
    :type posse_permalink: str
    :return: The original post permalink.
    :rtype: str
    """
    parsed_post = BeautifulSoup(posse_permalink, "lxml")

    # Get the post h-entry

    post_h_entry = parsed_post.select(".h-entry")

    original_post_url = None

    if post_h_entry:
        post_h_entry = post_h_entry[0]

        # select with u-url and u-uid
        if post_h_entry.select(".u-url .u-uid"):
            original_post_url = post_h_entry.select(".u-url .u-uid")[0].get("href")
            return original_post_url

        canonical_links = parsed_post.select("link[rel='canonical']")

        if canonical_links:
            original_post_url = canonical_links[0].get("href")
            return original_post_url

        # look for text with see original anchor text

        for link in parsed_post.select("a"):
            if link.text.lower() == "see original".lower():
                if link.get("href"):
                    original_post_url = link.get("href")

                    return original_post_url

        candidate_url = None

        last_text = post_h_entry.select(".e-content")

        if last_text:
            last_text = last_text[0].select("p")[-1]

            # if permashortlink citation
            # format = (url.com id)

            if re.search(r"\((.*?)\)", last_text.text):
                permashortlink = re.search(r"\((.*?)\)", last_text.text)

                permashortlink = "http://" + permashortlink.group(0) + "/" + permashortlink.group(1)

                candidate_url = permashortlink

        try:
            request = requests.get(candidate_url)
        except:
            # return None if URL could not be retrieved for verification
            return None

        parsed_candidate_url = BeautifulSoup(request.text, "lxml")

        all_hyperlinks = parsed_candidate_url.select("a")

        posse_domain = posse_permalink.split("/")[2]

        for link in all_hyperlinks:
            if "u-syndication" in link.get("class"):
                url_to_check = link.get("href")

                original_post_url = _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain)

                if original_post_url:
                    return original_post_url

        all_syndication_link_headers = parsed_post.select("link[rel='syndication']")

        for header in all_syndication_link_headers:
            if header.get("href") == posse_permalink:
                url_to_check = header.get("href")

                original_post_url = _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain)

                if original_post_url:
                    return original_post_url

    return None


def discover_author(url, page_contents=None):
    """
    Discover the author of a post per the IndieWeb Authorship specification.

    :param url: The URL of the post.
    :type url: str
    :param page_contents: The optional page contents to use. Specifying this value prevents a HTTP request being made to the URL.
    :type page_contents: str
    :return: A h-card of the post.
    :rtype: dict

    """
    if page_contents:
        full_page = mf2py.parse(doc=page_contents)
    else:
        full_page = mf2py.parse(url=url)

    preliminary_author = None

    h_entry = [e for e in full_page["items"] if e["type"] == ["h-entry"]]

    if h_entry and h_entry[0]["properties"].get("author"):
        preliminary_author = h_entry[0]["properties"]["author"][0]

    h_feed = [e for e in full_page["items"] if e["type"] == ["h-feed"]]

    if h_feed and h_feed[0]["properties"].get("author"):
        preliminary_author = h_entry[0]["properties"]["author"][0]

    author_page_url = None

    if preliminary_author and type(preliminary_author) == str:
        if preliminary_author.startswith("https://"):
            # author is url, further processing needed
            author_page_url = preliminary_author
        else:
            # author is name
            return preliminary_author

    if preliminary_author and type(preliminary_author) == dict:
        # author is h-card so the value can be returned
        return preliminary_author

    # if rel=author, look for h-card on the rel=author link
    if author_page_url is None and h_entry and h_entry[0].get("rels") and h_entry[0]["rels"].get("author"):
        rel_author = h_entry[0]["rels"]["author"]

        if rel_author:
            author_page_url = rel_author[0]

    # canonicalize author page
    if author_page_url:
        if author_page_url.startswith("//"):
            author_page_url = "http:" + author_page_url
        elif author_page_url.startswith("/"):
            author_page_url = url + author_page_url
        elif author_page_url.startswith("http"):
            author_page_url = author_page_url
        else:
            author_page_url = None

    if author_page_url is not None:
        new_h_card = mf2py.parse(url=author_page_url)

        # get rel me values from parsed object
        if new_h_card.get("rels") and new_h_card.get("rels").get("me"):
            rel_mes = new_h_card["rels"]["me"]
        else:
            rel_mes = []

        final_h_card = [e for e in new_h_card["items"] if e["type"] == "h-card"]

        if len(final_h_card) > 0:
            for card in final_h_card:
                for j in card["items"]:
                    if (
                        j.get("type")
                        and j.get("type") == ["h-card"]
                        and j["properties"]["url"] == rel_author
                        and j["properties"].get("uid") == j["properties"]["url"]
                    ):
                        h_card = j
                        return h_card

                    if j.get("type") and j.get("type") == ["h-card"] and j["properties"].get("url") in rel_mes:
                        h_card = j
                        return h_card

                    if j.get("type") and j.get("type") == ["h-card"] and j["properties"]["url"] == rel_author:
                        h_card = j
                        return h_card

    # no author found, return None
    return None


def get_post_type(h_entry, custom_properties=[]):
    """
    Return the type of a h-entry per the Post Type Discovery algorithm.

    :param h_entry: The h-entry whose type to retrieve.
    :type h_entry: dict
    :param custom_properties: The optional custom properties to use for the Post Type Discovery algorithm.
    :type custom_properties: list[tuple[str, str]]
    :return: The type of the h-entry.
    :rtype: str
    """
    post = h_entry.get("properties")

    if post is None:
        return "unknown"

    values_to_check = [
        ("rsvp", "rsvp"),
        ("in-reply-to", "reply"),
        ("repost-of", "repost"),
        ("like-of", "like"),
        ("video", "video"),
        ("photo", "photo"),
        ("summary", "summary"),
    ]

    for prop in custom_properties:
        if len(prop) == 2 and type(prop) == tuple:
            values_to_check.append(prop)
        else:
            raise Exception("custom_properties must be a list of tuples")

    for item in values_to_check:
        if post.get(item[0]):
            return item[1]

    post_type = "note"

    if post.get("name") is None or post.get("name")[0] == "":
        return post_type

    title = post.get("name")[0].strip().replace("\n", " ").replace("\r", " ")

    content = post.get("content")

    if content and content[0].get("text") and content[0].get("text")[0] != "":
        content = BeautifulSoup(content[0].get("text"), "lxml").get_text()

    if content and content[0].get("html") and content[0].get("html")[0] != "":
        content = BeautifulSoup(content[0].get("html"), "lxml").get_text()

    if not content.startswith(title):
        return "article"

    return "note"


def _syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain):
    if url_to_check == posse_permalink:
        return candidate_url

    if url_to_check and url_to_check.split("/")[2] == posse_domain:
        try:
            r = requests.get(url_to_check, timeout=10, allow_redirects=True)
        except:
            # handler will prevent exception due to timeout, if one occurs
            pass

        for url_item in r.history:
            if url_item.url == posse_permalink:
                return candidate_url

    return None
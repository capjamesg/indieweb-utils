"""
indieweb_utils - A Python library that provides building blocks
for people implementing IndieWeb applications.
"""

import re
from bs4 import BeautifulSoup
import requests
import mf2py

__version__ = "0.1.2"

def canonicalize_url(url, domain, full_url=None, protocol="https"):
    """
    Return a canonical URL for the given URL.

    :param url: The URL to canonicalize.
    :type url: str
    :param domain: The domain to use for the canonical URL.
    :type domain: str
    :param full_url: Optional full URL to use for the canonical URL.
    :type full_url: str or None
    :param protocol: Optional protocol to use for the canonical URL.
    :type protocol: str or None
    :return: The canonical URL.
    :rtype: str
    """

    if url.startswith("http://") or url.startswith("https://"):
        domain = url.split("/")[2]

        # remove port from domain

        domain = domain.split(":")[0]
        protocol = url.split("/")[0]

        return protocol + "//" + domain + "/" + "/".join(url.split("/")[3:])

    if ":" in domain:
        text_before_port = domain.split(":")[0]

        text_after_port = domain.split(":")[1].split("/")[0]

        domain = text_before_port + "/" + text_after_port

    final_result = ""

    if url.startswith("//"):
        final_result = protocol + ":" + domain.strip() + "/" + url
    elif url.startswith("/"):
        final_result = protocol + "://" + domain.strip() + "/" + url
    elif url.startswith("./"):
        final_result = full_url + url[1:]
    elif url.startswith("../"):
        final_result = protocol + "://" + domain.strip() + "/" + url[3:]
    else:
        final_result = protocol + "://" + url
    
    # replace ../ throughout url

    url_after_replacing_dots = ""

    to_check = final_result.replace(domain, "").replace(protocol + "://", "")

    for url_item in to_check.split("/"):
        if url_item == "..":
            # directory before ../
            directory = url_after_replacing_dots.split("/")[-1]
            url_after_replacing_dots = url_after_replacing_dots.replace(directory, "")
        else:
            url_after_replacing_dots += "/" + url_item

    url_after_replacing_dots = url_after_replacing_dots.lstrip("/")

    # replace ./ throughout url

    url_after_replacing_dots = url_after_replacing_dots.replace("./", "/")

    final_url = protocol + "://" + domain + "/" + url_after_replacing_dots.lstrip("/")

    return final_url

def discover_endpoints(url, headers_to_find):
    """
    Return a dictionary of specified endpoint locations for the given URL, if available.

    :param url: The URL to discover endpoints for.
    :type url: str
    :param headers_to_find: The headers to find.
    :type headers_to_find: dict[str, str]
    :return: The discovered endpoints.
    :rtype: dict[str, str]
    """
    response = {}

    endpoint_request = requests.get(url)

    http_link_headers = endpoint_request.headers.get("link")

    if http_link_headers:
        parsed_link_headers = requests.utils.parse_header_links(
            http_link_headers.rstrip('>').replace('>,<', ',<')
        )
    else:
        parsed_link_headers = []

    for header in parsed_link_headers:
        if header["rel"] in headers_to_find:
            response[header["rel"]] = header["url"]

    soup = BeautifulSoup(endpoint_request.text, "lxml")

    for link in soup.find_all("link"):
        if link.get("rel") in headers_to_find:
            response[link.get("rel")] = link.get("href")

    for response_url in response:
        if not response[response_url].startswith("https://") and not response[response_url].startswith("http://"):
            response.pop(response_url)

    return response

def discover_webmention_endpoint(target):
    """
    Return the webmention endpoint for the given target.

    :param target: The target to discover the webmention endpoint for.
    :type target: str
    :return: The discovered webmention endpoint.
    :rtype: str
    """
    if not target:
        return None, "No target specified."

    endpoints = discover_endpoints(target, ["webmention"])

    endpoint = endpoints.get("webmention", None)

    if endpoint is None:
        message = "No webmention endpoint could be found for this resource."
        return None, message

    invalid_endpoints = ("0.0.0.0", "127.0.0.1", "localhost")

    if endpoint in invalid_endpoints:
        message = "This resource is not supported."
        return None, message

    if endpoint == "":
        endpoint = target

    valid_starts = ("http://", "https://", "/")

    if not any(endpoint.startswith(valid_start) for valid_start in valid_starts):
        endpoint = "/".join(target.split("/")[:-1]) + "/" + endpoint

    if endpoint.startswith("/"):
        endpoint = "https://" + target.split("/")[2] + endpoint
    
    return endpoint, ""

def indieauth_callback_handler(
        code,
        state,
        token_endpoint,
        code_verifier,
        session_state,
        me,
        callback_url,
        client_id,
        required_scopes
    ):
    """
    Exchange a callback 'code' for an authentication token.

    :param code: The callback 'code' to exchange for an authentication token.
    :type code: str
    :param state: The state provided by the authentication server in the callback response.
    :type state: str
    :param token_endpoint: The token endpoint to use for exchanging the callback 'code' for an authentication token.
    :type token_endpoint: str
    :param code_verifier: The code verifier to use for exchanging the callback 'code' for an authentication token.
    :type code_verifier: str
    :param session_state: The state stored in session used to verify the callback state is valid.
    :type session_state: str
    :param me: The URL of the user's profile.
    :type me: str
    :param callback_url: The callback URL used in the original authentication request.
    :type callback_url: str
    :param client_id: The client ID used in the original authentication request.
    :type client_id: str
    :param required_scopes: The scopes required for the application to work. This list should not include optional scopes.
    :type required_scopes: list[str]
    :return: A message indicating the result of the callback (success or failure) and the token endpoint response. The endpoint response will be equal to None if the callback failed.
    :rtype: tuple[str, dict]
    """

    if state != session_state:
        message = "Your authentication failed. Please try again."
        return message, None

    data = {
        "code": code,
        "redirect_uri": callback_url,
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier
    }

    headers = {
        "Accept": "application/json"
    }

    try:
        r = requests.post(token_endpoint, data=data, headers=headers)
    except:
        message = "Your token endpoint server could not be accessed."
        return message, None
    
    if r.status_code != 200:
        message = "There was an error with your token endpoint server."
        return message, None

    # remove code verifier from session because the authentication flow has finished

    if me is None:
        message = "An invalid me value was provided."

        return message, None

    if r.json().get("me").strip("/") != me.strip("/"):
        message = "Your domain is not allowed to access this website."

        return message

    granted_scopes = r.json().get("scope").split(" ")

    if r.json().get("scope") == "" or \
            any(scope not in granted_scopes for scope in required_scopes):
        message = f"You need to grant {', '.join(required_scopes).strip(', ')} access to use this tool."
        return message, None

    return None, r.json()

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
        ("summary", "summary")
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

    h_entry = [e for e in full_page['items'] if e['type'] == ['h-entry']]

    if h_entry and h_entry[0]["properties"].get('author'):
        preliminary_author = h_entry[0]["properties"]['author'][0]

    h_feed = [e for e in full_page['items'] if e['type'] == ['h-feed']]

    if h_feed and h_feed[0]["properties"].get('author'):
        preliminary_author = h_entry[0]["properties"]['author'][0]

    author_page_url = None
        
    if preliminary_author and type(preliminary_author) == str:
        if preliminary_author.startswith('https://'):
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
        rel_author = h_entry[0]['rels']['author']

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
            rel_mes = new_h_card['rels']['me']
        else:
            rel_mes = []

        final_h_card = [e for e in new_h_card['items'] if e['type'] == 'h-card']

        if len(final_h_card) > 0:
            for card in final_h_card:
                for j in card["items"]:
                    if j.get('type') and j.get('type') == ['h-card'] and \
                            j['properties']['url'] == rel_author and \
                            j['properties'].get('uid') == j['properties']['url']:
                        h_card = j
                        return h_card

                    if j.get('type') and j.get('type') == ['h-card'] and j['properties'].get('url') in rel_mes:
                        h_card = j
                        return h_card

                    if j.get('type') and j.get('type') == ['h-card'] and j['properties']['url'] == rel_author:
                        h_card = j
                        return h_card

    # no author found, return None
    return None

def syndication_check(url_to_check, posse_permalink, candidate_url, posse_domain):
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

def discover_original_post(posse_permalink):
    """
    Find the original version of a post per the Original Post Discovery algorithm.

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
                
                original_post_url = syndication_check(
                    url_to_check,
                    posse_permalink,
                    candidate_url,
                    posse_domain
                )

                if original_post_url:
                    return original_post_url
        
        all_syndication_link_headers = parsed_post.select("link[rel='syndication']")

        for header in all_syndication_link_headers:
            if header.get("href") == posse_permalink:
                url_to_check = header.get("href")
                
                original_post_url = syndication_check(
                    url_to_check,
                    posse_permalink,
                    candidate_url,
                    posse_domain
                )

                if original_post_url:
                    return original_post_url
    
    return None

def get_reply_context(url, twitter_bearer_token=None):
    """
    Generate reply context for use on your website based on a URL.

    :param url: The URL of the post to generate reply context for.
    :type url: str
    :param twitter_bearer_token: The optional Twitter bearer token to use. This token is used to retrieve a Tweet from Twitter's API if you want to generate context using a Twitter URL.
    :type twitter_bearer_token: str
    :return: was successful (bool), reply context (dict) or error (dict), page accepts webmention (bool)
    :rtype: list
    """
    h_entry = None
    photo_url = None
    site_supports_webmention = False

    http_headers = {
        'Accept': 'text/html',
        'User-Agent': 'indieweb_utils'
    }

    if url.startswith("https://") or url.startswith("http://"):
        try:
            page_content = requests.get(url, timeout=10, verify=False, headers=http_headers)
        except:
            return True, {
                "error": "Page content could not be retrieved."
            }

        if page_content.status_code != 200:
            return True, {
                "error": page_content.status_code
            }

        parsed = mf2py.parse(page_content.text)

        supports_webmention = requests.get(
            f"https://webmention.jamesg.blog/discover?target={url}"
        )

        if supports_webmention.status_code == 200:
            if supports_webmention.json().get("success") == True:
                site_supports_webmention = True

        domain = url.replace("https://", "").replace("http://", "").split("/")[0]

        if parsed["items"] and parsed["items"][0]["type"] == ["h-entry"]:
            h_entry = parsed["items"][0]

            author_url = None
            author_name = None
            author_image = None

            if h_entry["properties"].get("author"):
                if type(h_entry["properties"]["author"][0]) == dict and h_entry["properties"]["author"][0].get("type") == ["h-card"]:
                    if h_entry['properties']['author'][0]['properties'].get('url'):
                        author_url = h_entry['properties']['author'][0]['properties']['url'][0] 
                    else:
                        author_url = url

                    if h_entry['properties']['author'][0]['properties'].get('name'):
                        author_name = h_entry['properties']['author'][0]['properties']['name'][0]
                    else:
                        author_name = None
                    
                    if h_entry['properties']['author'][0]['properties'].get('photo'):
                        author_image = h_entry['properties']['author'][0]['properties']['photo'][0]
                    else:
                        author_image = None
                elif type(h_entry["properties"]["author"][0]) == str:
                    if h_entry["properties"].get("author") and h_entry["properties"]["author"][0].startswith("/"):
                        author_url = url.split("/")[0] + "//" + domain + h_entry["properties"].get("author")[0]

                    author = mf2py.parse(requests.get(author_url, timeout=10, verify=False).text)
                    
                    if author["items"] and author["items"][0]["type"] == ["h-card"]:
                        author_url = h_entry['properties']['author'][0]

                        if author['items'][0]['properties'].get('name'):
                            author_name = h_entry['properties']['author'][0]['properties']['name'][0]
                        else:
                            author_name = None
                        
                        if author['items']['properties'].get('photo'):
                            author_image = h_entry['properties']['author'][0]['properties']['photo'][0]
                        else:
                            author_image = None

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
                    author_image = None

                post_body = " ".join(post_body.split(" ")[:75]) + " ..."
            elif h_entry["properties"].get("content"):
                post_body = h_entry["properties"]["content"]

                post_body = " ".join(post_body.split(" ")[:75]) + " ..."
            else:
                post_body = None

            # get p-name
            if h_entry["properties"].get("name"):
                p_name = h_entry["properties"]["name"][0]
            else:
                p_name = None

            if author_url is not None and \
                    (not author_url.startswith("https://") and not author_url.startswith("http://")):
                author_url = "https://" + author_url

            if not author_name and author_url:
                author_name = author_url.split("/")[2]

            post_photo_url = None
            post_video_url = None

            if h_entry["properties"].get("photo"):
                post_photo_url = canonicalize_url(h_entry["properties"]["photo"][0], domain, url)

            if h_entry["properties"].get("video"):
                post_video_url = canonicalize_url(h_entry["properties"]["video"][0], domain, url)

            # look for featured image to display in reply context
            if post_photo_url is None:
                if soup.find("meta", property="og:image") and soup.find("meta", property="og:image")["content"]:
                    post_photo_url = soup.find("meta", property="og:image")["content"]
                elif soup.find("meta", property="twitter:image") and soup.find("meta", property="twitter:image")["content"]:
                    post_photo_url = soup.find("meta", property="twitter:image")["content"]

            h_entry = {
                "type": "entry",
                "author": {
                    "type": "card",
                    "url": author_url,
                    "name": author_name,
                    "photo": author_image
                },
                "name": p_name,
                "url": url,
                "content": {
                    "html": post_body
                }
            }

            if post_photo_url:
                h_entry["post_photo_url"] = post_photo_url

            if post_video_url:
                h_entry["post_video_url"] = post_video_url

            return True, h_entry, site_supports_webmention

        elif parsed["items"] and parsed["items"][0]["type"] == ["h-card"]:
            h_card = parsed["items"][0]

            if h_card["properties"].get("name"):
                author_name = h_card['properties']['name'][0]
            else:
                author_name = None

            if h_card["properties"].get("photo"):
                author_image = h_card['properties']['photo'][0]
                if author_image.startswith("//"):
                    author_image = "https:" + author_image
                elif author_image.startswith("/"):
                    author_image = url.split("/")[0] + "//" + domain + author_image
                elif author_image.startswith("http://") or author_image.startswith("https://"):
                    author_image = author_image
                else:
                    author_image = "https://" + domain + "/" + author_image
            else:
                author_image = None

            if h_card["properties"].get("note"):
                post_body = h_card['properties']['note'][0]
            else:
                post_body = None

            h_entry = {
                "type": "entry",
                "author": {
                    "type": "card",
                    "url": url,
                    "name": author_name,
                    "photo": author_image
                },
                "url": url,
                "content": {
                    "html": post_body
                }
            }
            
            return True, h_entry, site_supports_webmention
            
        h_entry = {}

        if url.startswith("https://twitter.com") and twitter_bearer_token is not None:
            site_supports_webmention = False
            tweet_uid = url.strip("/").split("/")[-1]

            headers = {
                "Authorization": f"Bearer {twitter_bearer_token}"
            }

            r = requests.get(
                f"https://api.twitter.com/2/tweets/{tweet_uid}?tweet.fields=author_id",
                headers=headers,
                timeout=10, 
                verify=False
            )

            if r and r.status_code != 200:
                return {}, None

            base_url = f"https://api.twitter.com/2/users/{r.json()['data'].get('author_id')}"

            get_author = requests.get(
                f"{base_url}?user.fields=url,name,profile_image_url,username",
                headers=headers,
                timeout=10,
                verify=False
            )

            if get_author and get_author.status_code == 200:
                photo_url = get_author.json()["data"].get("profile_image_url")
                author_name = get_author.json()["data"].get("name")
                author_url = "https://twitter.com/" + get_author.json()["data"].get("username")
            else:
                photo_url = None
                author_name = None
                author_url = None

            h_entry = {
                "type": "entry",
                "author": {
                    "type": "card",
                    "url": author_url,
                    "name": author_name,
                    "photo": photo_url
                },
                "url": url,
                "content": {
                    "text": r.json()["data"].get("text")
                }
            }

            return True, h_entry, site_supports_webmention

        soup = BeautifulSoup(requests.get(url, headers=http_headers).text, "lxml")

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
                p_tag = None
        else:
            p_tag = None

        if soup.select('.e-content'):
            p_tag = soup.select('.e-content')[0]

            # get first paragraph
            if p_tag:
                p_tag = p_tag.find("p")
                if p_tag:
                    p_tag = p_tag.text

                p_tag = " ".join([w for w in p_tag.split(" ")[:75]]) + " ..."
            else:
                p_tag = ""

        post_photo_url = None

        # look for featured image to display in reply context
        if soup.select('.u-photo'):
            post_photo_url = soup.select('.u-photo')[0]['src']
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
                photo_url = None
        else:
            photo_url = None

        if not domain.startswith("https://") and not domain.startswith("http://"):
            author_url = "https://" + domain

            h_entry = {
                "type": "entry",
                "author": {
                    "type": "card",
                    "url": "https://" + domain,
                    "photo": photo_url
                },
                "url": "https://" + domain,
                "content": {
                    "text": p_tag
                }
            }
            
        if post_photo_url:
            h_entry["post_photo_url"] = post_photo_url

        return True, h_entry, site_supports_webmention

    return True, h_entry, site_supports_webmention

def is_authenticated(token_endpoint, headers, session, approved_user=None):
    """
    Check if a user has provided a valid Authorization header or access token in session. Designed for use with Flask.

    :param token_endpoint: The token endpoint of the user's IndieAuth server.
    :param headers: The headers sent by a request.
    :param session: The session object from a Flask application.
    :param approved_user: The optional URL of the that is approved to use the API.
    :return: True if the user is authenticated, False otherwise.
    :rtype: bool
    """
    if headers.get("Authorization") is not None:
        access_token = headers.get("Authorization").split(" ")[-1]
    elif session.get("access_token"):
        access_token = session.get("access_token")
    else:
        return False

    check_token = requests.get(token_endpoint, headers={"Authorization": "Bearer " + access_token})

    if check_token.status_code != 200 or not check_token.json().get("me"):
        return False

    if approved_user is not None and check_token.status_code != 200 and check_token.json()["me"] != approved_user:
        return False

    return True

def send_webmention(source, target, me=None):
    if not source and not target:
        message = {
            "title": "Please enter a source and target.",
            "description": "Please enter a source and target.",
            "url": target,
            "status": "failed"
        }

        return message


    if not target.startswith("https://"):
        message = {
            "title": "Error: Target must use https:// protocol.",
            "description": "Target must use https:// protocol.",
            "url": target,
            "status": "failed"
        }

        return message

    # if domain is not approved, don't allow access
    if me is not None:
        target_domain = target.split("/")[2]

        if "/" in me.strip("/"):
            raw_domain = me.split("/")[2]
        else:
            raw_domain = me

        if not target_domain.endswith(raw_domain):
            message = {
                "title": f"Error: Target must be a {me} post.",
                "description": f"Target must be a {me} post.",
                "url": target,
                "status": "failed"
            }

            return message

    # set up bs4
    r = requests.get(target, allow_redirects=True)

    soup = BeautifulSoup(r.text, "lxml")
    
    link_header = r.headers.get("Link")

    endpoint = None

    if link_header:
        parsed_links = requests.utils.parse_header_links(link_header.rstrip('>').replace('>,<', ',<'))

        for link in parsed_links:
            if "webmention" in link["rel"]:
                endpoint = link["url"]
                break

    if endpoint is None:
        for item in soup():
            if item.name == "a" and item.get("rel") and item["rel"][0] == "webmention":
                endpoint = item.get("href")
                break

            if item.name == "link" and item.get("rel") and item["rel"][0] == "webmention":
                endpoint = item.get("href")
                break

    invalid_endpoints = ("0.0.0.0", "127.0.0.1", "localhost")

    if endpoint in invalid_endpoints:
        message = {
            "title": "Error:" + "Your endpoint is not supported.",
            "description": "Your endpoint is not supported.",
            "url": target,
            "status": "failed"
        }

        return message

    if endpoint is None:
        message = {
            "title": "Error:" + "No endpoint could be found for this resource.",
            "description": "No endpoint could be found for this resource.",
            "url": target,
            "status": "failed"
        }

        return message


    if endpoint == "":
        endpoint = target

    valid_start = ("https://", "http://", "/")

    if not any(endpoint.startswith(start) for start in valid_start):
        if r.history:
            endpoint = "/".join(r.url.split("/")[:-1]) + "/" + endpoint
        else:
            endpoint = "/".join(target.split("/")[:-1]) + "/" + endpoint

    if endpoint.startswith("/"):
        if r.history:
            endpoint = "https://" + r.url.split("/")[2] + endpoint
        else:
            endpoint = "https://" + target.split("/")[2] + endpoint
    
    # make post request to endpoint with source and target as values
    r = requests.post(
        endpoint, 
        data={
            "source": source,
            "target": target
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    message = str(r.json()["message"])

    if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
        message = {
            "title": message,
            "description": message,
            "url": target,
            "status": "success"
        }
    else:
        message = {
            "title": "Error: " + message,
            "description": "Error: " + message,
            "url": target,
            "status": "failed"
        }

    return message
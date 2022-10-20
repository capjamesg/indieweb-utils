from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib import parse as url_parse

import requests
from bs4 import BeautifulSoup

from indieweb_utils.webmentions.discovery import discover_endpoints

from ..utils.urls import canonicalize_url


class WebmentionValidationError(Exception):
    pass


class WebmentionIsGone(Exception):
    pass


class NoTokenEndpointForPrivateWebmention(Exception):
    pass


@dataclass
class WebmentionCheckResponse:
    webmention_is_valid: bool
    vouch_check_has_passed: bool
    source_text: str
    source_tree: BeautifulSoup


def _process_vouch(vouch: str, source: str, vouch_list: List[str]) -> bool:
    """
    use vouch to flag webmentions for moderation
    see Vouch spec for more: https://indieweb.org/Vouch
    by default, webmention should require moderation
    if a vouch is valid, webmention does not need moderation
    """

    moderate = True

    if vouch:
        vouch_domain = url_parse.urlparse(vouch).netloc

        if vouch_domain in vouch_list:
            try:
                r = requests.get(vouch, timeout=5)
            except requests.exceptions.RequestException:
                return moderate

            soup = BeautifulSoup(r.text, "html.parser")

            # find hyperlink with source
            # required for a vouch to be valid
            for anchor in soup.find_all("a"):
                if anchor.get("href"):
                    if anchor["href"] == source:
                        moderate = False

    return moderate


def _validate_headers(request_item):
    if request_item.headers.get("Content-Length"):
        if int(request_item.headers["Content-Length"]) > 10000000:
            raise WebmentionValidationError("Source is too large.")

    if "text/html" not in request_item.headers["Content-Type"]:
        raise WebmentionValidationError("This endpoint only supports HTML webmentions.")

    return True


def _check_for_link_to_target(validation_source: requests.Response, target) -> bool:
    soup = BeautifulSoup(validation_source.text, "html.parser")

    all_anchors = soup.find_all("a")
    contains_valid_link_to_target = False

    target_domain = url_parse.urlparse(target).netloc

    for anchor in all_anchors:
        if anchor.get("href"):
            canoncalized = canonicalize_url(anchor["href"], target_domain, target)
            if canoncalized == target:
                contains_valid_link_to_target = True

    if target in validation_source.text:
        contains_valid_link_to_target = True

    return contains_valid_link_to_target


def _webmention_head_request(session: requests.Session, source: str = "") -> Tuple[requests.Response, bool]:
    try:
        check_source_size = session.head(source, timeout=5)

        validated_headers = _validate_headers(check_source_size)
    except requests.exceptions.TooManyRedirects:
        raise WebmentionValidationError("Source redirected too many times.")
    except requests.exceptions.Timeout:
        raise WebmentionValidationError("Source timed out.")
    except requests.exceptions.RequestException:
        # pass because HEAD request might not be recognised / processed by the client
        pass

    return check_source_size, validated_headers


def _validate_private_webmention(source: str, session: requests.Session, code: str) -> str:
    source_token_endpoint = discover_endpoints(source, ["token_endpoint"])

    if source_token_endpoint.get("token_endpoint") is None:
        raise NoTokenEndpointForPrivateWebmention(
            "The webmention sent is a private webmention but the source has no token endpoint."
        )

    token_endpoint = source_token_endpoint["token_endpoint"]

    try:
        token_request = session.post(token_endpoint, data={"grant_type": "authorization_code", "code": code})
    except requests.exceptions.RequestException:
        raise WebmentionValidationError(
            "Token endpoint of source could not be accessed while trying to validate private webmention."
        )

    if token_request.status_code != 200:
        raise WebmentionValidationError(
            "Token endpoint of source returned an error while trying to validate private webmention."
        )

    return token_request.json().get("access_token")


def _retrieve_webmention_target(
    source: str, code: str = None, target_request: Optional[requests.Response] = None
) -> Tuple[BeautifulSoup, str]:
    # Only allow 3 redirects before raising an error

    if target_request:
        validated_headers = _validate_headers(target_request)

        get_source_for_validation = target_request
    else:
        session = requests.Session()
        session.max_redirects = 3

        validated_headers = False

        request_headers = {}

        if code:
            access_token = _validate_private_webmention(source, session, code)

            request_headers = {"Authorization": f"Bearer {access_token}"}

        try:
            get_source_for_validation = session.get(source, headers=request_headers)
        except requests.exceptions.RequestException:
            raise WebmentionValidationError("Source could not be retrieved.")

        check_source_size, validated_headers = _webmention_head_request(session, source)

    if validated_headers is False:
        validated_headers = _validate_headers(check_source_size)

    if get_source_for_validation.status_code == 410:
        raise WebmentionIsGone("Webmention source returned 410 Gone code.")

    if check_source_size.status_code != 200:
        raise WebmentionValidationError(f"Webmention source returned {check_source_size.status_code} code.")

    parse_page = BeautifulSoup(get_source_for_validation.text, "html.parser")

    return parse_page, get_source_for_validation.text


def validate_webmention(
    source: str,
    target: str,
    code: str = None,
    vouch: str = "",
    vouch_list: List[str] = [],
    target_request: requests.Response = None,
) -> WebmentionCheckResponse:
    """
    Check if a webmention is valid.

    :refs: https://indieweb.org/Webmention
    :refs: https://indieweb.org/Private-Webmention
    :refs: https://indieweb.org/Vouch

    :param source: The source URL of the webmention.
    :type source: str
    :param target: The target URL of the webmention.
    :type target: str
    :param code: The code to use to validate a private webmention.
    :type code: str
    :param vouch: The vouch URL of the webmention.
    :type vouch: str
    :param vouch_list: A list of vouch domains.
    :type vouch_list: list
    :return: Boolean to indicate webmention is valid, boolean
        stating whether the vouch check has passed.
    :rtype: bool, bool

    Here is an example of a workflow for validating a webmention:

    .. code-block:: python

        import indieweb_utils

        source = "https://jamesg.blog/"
        target = "https://jamesg.blog/mugs/"

        webmention_is_valid = indieweb_utils.validate_webmention(
            source, target
        )

        print(webmention_is_valid) # Should return True

    :raises WebmentionValidationError: Webmention is invalid.
    :raises WebmentionIsGone: Webmention source returns a 410 Gone code.
    :raises NoTokenEndpointForPrivateWebmention: Webmention is private but source has no token endpoint.
    """

    if source.strip("/") == target.strip("/"):
        raise WebmentionValidationError("Source and target cannot be the same URL.")

    source_protocol = url_parse.urlparse(source).scheme
    target_protocol = url_parse.urlparse(target).scheme

    if source_protocol not in ["http", "https"]:
        raise WebmentionValidationError("Source must use either a http:// or https:// URL scheme.")

    if target_protocol not in ["http", "https"]:
        raise WebmentionValidationError("Target must use either a http:// or https:// URL scheme.")

    parsed_page_html_tree, page_html = _retrieve_webmention_target(source, code, target_request)

    # get all <link> tags
    meta_links = parsed_page_html_tree.find_all("link")

    for link in meta_links:
        # use meta http-equiv status spec to detect 410s https://indieweb.org/meta_http-equiv_status
        # detecting http-equiv status 410s is required by the webmention spec
        if link.get("http-equiv", "") == "Status" and link.get("content", "") == "410 Gone":
            raise WebmentionIsGone("Webmention source returned 410 Gone code.")

    contains_valid_link_to_target = _check_for_link_to_target(parsed_page_html_tree, target)

    # Might want to comment out this if statement for testing
    if not contains_valid_link_to_target:
        raise WebmentionValidationError("Source does not contain a link to target.")

    moderate = _process_vouch(vouch, source, vouch_list)

    return WebmentionCheckResponse(
        webmention_is_valid=True,
        vouch_check_has_passed=moderate,
        source_text=page_html,
        source_tree=parsed_page_html_tree,
    )

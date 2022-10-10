"""
Utilities to aid the implementation of various IndieWeb specifications and functionalities.
"""

# Imports added for API backwards compatibility

from .feeds import FeedUrl, discover_h_feed, discover_web_page_feeds
from .indieauth import (
    _validate_indieauth_response,
    generate_auth_token,
    get_h_app_item,
    get_profile,
    get_valid_relmeauth_links,
    is_authenticated,
    redeem_code,
    validate_access_token,
    validate_authorization_response,
)
from .indieauth.flask import IndieAuthCallbackResponse, indieauth_callback_handler
from .posts.discovery import discover_author, discover_original_post, get_post_type
from .posts.representative_h_card import get_representative_h_card
from .replies import ReplyContext, get_reply_context
from .utils.autotag import autolink_tags
from .utils.url_summary import InvalidURL, get_url_summary
from .utils.urls import canonicalize_url
from .webmentions import (
    SendWebmentionResponse,
    discover_endpoints,
    discover_webmention_endpoint,
    send_webmention,
    validate_webmention,
)

__version__ = "0.3.1"

# add for backwards compatibility
_discover_endpoints = discover_endpoints

__all__ = [
    "discover_web_page_feeds",
    "discover_author",
    "discover_original_post",
    "get_post_type",
    "get_reply_context",
    "canonicalize_url",
    "discover_webmention_endpoint",
    "send_webmention",
    "get_representative_h_card",
    "validate_webmention",
    "is_authenticated",
    "indieauth_callback_handler",
    "IndieAuthCallbackResponse",
    "SendWebmentionResponse",
    "FeedUrl",
    "ReplyContext",
    "get_profile",
    "get_h_app_item",
    "validate_access_token",
    "_validate_indieauth_response",
    "redeem_code",
    "get_valid_relmeauth_links",
    "validate_authorization_response",
    "autolink_tags",
    "discover_h_feed",
    "generate_auth_token",
    "get_url_summary",
    "InvalidURL",
    "discover_endpoints",
    "_discover_endpoints",
]

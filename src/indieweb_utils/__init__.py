"""
Utilities to aid the implementation of various IndieWeb specifications and functionalities.
"""

# Imports added for API backwards compatibility

from .feeds import FeedUrl, discover_h_feed, discover_web_page_feeds
from .indieauth import (
    _validate_indieauth_response,
    discover_indieauth_endpoints,
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
from .indieauth.scopes import SCOPE_DEFINITIONS
from .posts.discovery import discover_author, discover_original_post, get_post_type
from .posts.in_reply_to import get_reply_urls
from .posts.page_name import get_page_name
from .posts.posse import get_syndicated_copies
from .posts.representative_h_card import get_representative_h_card
from .replies import ReplyContext, get_reply_context
from .rsd import rsd_discovery
from .trackback import (
    ERROR_PING,
    SUCCESSFUL_PING,
    discover_trackback_url,
    process_trackback,
    rsd_trackback_discovery,
    send_trackback,
)
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

__version__ = "0.7.1"

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
    "get_syndicated_copies",
    "discover_endpoint",
    "get_reply_urls",
    "discover_endpoint",
    "autolink_tags",
    "discover_h_feed",
    "generate_auth_token",
    "get_url_summary",
    "InvalidURL",
    "discover_endpoints",
    "_discover_endpoints",
    "get_page_name",
    "SCOPE_DEFINITIONS",
    "generate_auth_token",
    "discover_indieauth_endpoints",
    "rsd_discovery",
    "rsd_trackback_discovery",
    "discover_trackback_url",
    "send_trackback",
    "process_trackback",
    "SUCCESSFUL_PING",
    "ERROR_PING",
]

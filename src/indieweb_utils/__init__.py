# Imports added for API backwards compatibility

from .feeds import FeedUrl, discover_web_page_feeds
from .indieauth import (
    _validate_indieauth_response,
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
from .posts.page_name import get_page_name
from .posts.representative_h_card import get_representative_h_card
from .replies import ReplyContext, get_reply_context
from .utils.urls import canonicalize_url
from .webmentions import (
    SendWebmentionResponse,
    discover_webmention_endpoint,
    send_webmention,
    validate_webmention,
)

__version__ = "0.2.0"

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
]

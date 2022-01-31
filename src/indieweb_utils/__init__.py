# Imports added for API backwards compatibility
from .feeds import discover_web_page_feeds, FeedUrl
from .posts.discovery import discover_author, discover_original_post, get_post_type
from .posts.representative_h_card import get_representative_h_card
from .indieauth.flask import is_authenticated, indieauth_callback_handler, IndieAuthCallbackResponse
from .replies import get_reply_context, ReplyContext
from .utils.urls import canonicalize_url
from .webmentions import (
    discover_webmention_endpoint,
    send_webmention,
    validate_webmention,
    SendWebmentionResponse
)
from .indieauth import (
    _validate_indieauth_response,
    get_profile,
    get_h_app_item,
    validate_access_token,
    is_authenticated,
    redeem_code
)

__version__ = "0.1.2"

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
    "redeem_code"
]

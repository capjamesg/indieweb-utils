# Imports added for API backwards compatibility
from .feeds import discover_web_page_feeds
from .posts.discovery import discover_author, discover_original_post, get_post_type
from .replies import get_reply_context
from .utils.urls import canonicalize_url
from .webmentions import (
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
    "validate_webmention",
]

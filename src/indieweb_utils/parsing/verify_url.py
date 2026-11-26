from urllib.parse import urlparse
from rfc3986 import is_valid_uri as rfc3986_is_valid_uri
import ipaddress

def check_if_url_is_safe(url):
    parsed = urlparse(url)
    ip = None

    try:
        ip = ipaddress.ip_address(parsed.hostname)
    except:
        pass

    if ip and not ip.is_global:
        raise Exception("URL is not valid.")
    
    if ip and (
        endpoint.is_private is True
        or endpoint.is_multicast is True
        or endpoint_as_ip.is_loopback is True
        or endpoint_as_ip.is_unspecified is True
        or endpoint_as_ip.is_reserved is True
        or endpoint_as_ip.is_link_local is True
    ):
        raise Exception("URL is not valid.")


    if (
        parsed.hostname == "localhost"
        or parsed.scheme not in ["http", "https"]
        or parsed.username
        or parsed.password
        or parsed.port
    ):
        raise Exception("URL is not valid.")

    if not rfc3986_is_valid_uri(
        url, require_scheme=True, require_authority=True
    ):
        raise Exception("URL is not valid.")

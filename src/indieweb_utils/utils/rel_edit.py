from indieweb_utils.webmentions.discovery import discover_endpoints, _find_links_html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from ..constants import USER_AGENT


def discover_edit_links(url: str, request: requests.Response = None):
    if not request:
        try:
            request = requests.get(url, headers={"User-Agent": USER_AGENT, "timeout": "5"})
        except requests.exceptions.RequestException:
            raise Exception("Could not connect to the specified URL.")

    domain = urlparse(url).netloc

    bs4_html = BeautifulSoup(request.text, "html.parser")

    rel_link_headers = discover_endpoints(url, ["edit"], request=request, bs4_html=bs4_html)

    rel_link_headers.update(_find_links_html(body=request.text, target_headers=["edit"], domain=domain, html_tag=["a"]))

    return rel_link_headers

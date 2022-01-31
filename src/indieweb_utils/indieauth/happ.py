from dataclasses import dataclass
from urllib.parse import urlparse as parse_url

from bs4 import BeautifulSoup

from ..utils.urls import _is_http_url


@dataclass
class ApplicationInfo:
    name: str
    logo: str
    url: str
    summary: str


def get_h_app_item(
    web_page: str,
    client_id: str,
    redirect_uri: str,
) -> ApplicationInfo:
    """
    Get the h-app item from the web page.

    :param web_page: The web page to parse.
    :type web_page: str
    :param client_id: The client id of your application.
    :type client_id: str
    :param redirect_uri: The redirect uri specified by the client.
    :type redirect_uri: str
    :return: The h-app item.
    :rtype: ApplicationInfo
    """

    redirect_uri_domain = parse_url(redirect_uri).netloc
    redirect_uri_scheme = parse_url(redirect_uri).scheme

    app_name = ""
    app_url = ""
    app_logo = ""
    app_summary = ""

    h_x_app = BeautifulSoup(web_page, "lxml")
    h_app_item = h_x_app.select(".h-app")

    if not h_app_item:
        h_app_item = h_x_app.select(".h-x-app")

    if h_app_item:
        h_app_item = h_app_item[0]
        logo = h_app_item.select(".u-logo")
        name = h_app_item.select(".p-name")
        url = h_app_item.select(".u-url")
        summary = h_app_item.select(".p-summary")

        if name and name[0].text.strip() != "":
            app_name = name[0].text
        else:
            app_name = client_id

        if logo and len(logo) > 0 and logo[0].get("src"):
            logo_to_validate = logo[0].get("src")
            if logo[0].get("src").startswith("/"):
                logo_to_validate = redirect_uri_scheme + redirect_uri_domain.strip("/") + logo[0].get("src")
            elif logo[0].get("src").startswith("//"):
                logo_to_validate = redirect_uri_scheme + logo[0].get("src")
            elif _is_http_url(logo[0].get("src")):
                logo_to_validate = logo[0].get("src")
            else:
                logo_to_validate = redirect_uri_scheme + redirect_uri_domain.strip("/") + "/" + logo[0].get("src")

            app_logo = logo_to_validate

        if url and url[0].get("href").strip() != "":
            app_url = url[0].get("href")
        else:
            app_url = client_id

        if summary and summary[0].text.strip() != "":
            app_summary = summary[0].text

    return ApplicationInfo(name=app_name, logo=app_logo, url=app_url, summary=app_summary)

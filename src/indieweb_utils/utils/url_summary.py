import re
from urllib.parse import urlparse

from .url_summary_templates import URL_SUMMARY_TEMPLATES
from .urls import canonicalize_url


class InvalidURL(Exception):
    """
    The provided URL is incorrectly formatted.
    """

    pass


def get_url_summary(url: str, custom_templates: list = None):
    """
    Return a text summary for given `url`.

    :param url: The URL to summarize.
    :param custom_templates: A list of tuples with patterns against which to check
        when generating a summary associated with results to return.
    :return: A summary of the URL.
    :rtype: str

    .. code-block:: python

        import indieweb_utils

        # a dictionary of custom patterns against which to match during the lookup
        custom_properties = {
            "jamesg.blog": [
                (r"coffee/maps/(?P<location>.+)", "A map of {location} coffee shops on jamesg.blog")
            ]
        }

        summary = indieweb_utils.get_summary("https://github.com/capjamesg/indieweb-utils/pulls/1")

        print(summary) # "A comment on a pull request in the indieweb-utils GitHub repository"

        summary = indieweb_utils.get_summary("https://jamesg.blog/coffee/maps/london")

        print(summary) # "A map of london coffee shops on jamesg.blog"
    """

    url = canonicalize_url(url)

    if custom_templates is None:
        custom_templates = []

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    domain = domain.lstrip("www.")

    if not domain:
        raise InvalidURL("The provided URL is incorrectly formatted.")

    for pattern, summary in URL_SUMMARY_TEMPLATES.get(domain, []) + custom_templates:
        if match := re.match(pattern, parsed_url.path.lstrip("/")):
            return summary.format(**match.groupdict())

    return "A post by " + domain

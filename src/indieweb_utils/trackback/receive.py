from urllib.parse import urlparse

SUCCESSFUL_PING = """
<?xml version="1.0" encoding="iso-8859-1"?>
<response>
    <error>0</error>
</response>
"""

ERROR_PING = """
<?xml version="1.0" encoding="iso-8859-1"?>
<response>
    <error>1</error>
    <message>{}</message>
</response>
"""


def process_trackback(url: str, content_type: str = None, method: str = None, valid_domains: list = None):
    """
    Validate and process a trackback request.

    :param url: The URL to send the trackback to.
    :param content_type: The content type of the request.
    :param method: The request method.
    :param valid_domains: A list of valid domains to accept trackbacks from.
    :returns: The trackback response.

    Example:

        from indieweb_utils import process_trackback

        process_trackback(
            'http://example.com/post/123',
            content_type='application/x-www-form-urlencoded',
            method='POST'
        )
    """

    if method and method != "POST":
        return ERROR_PING.format("Invalid request method.")

    if content_type and content_type != "application/x-www-form-urlencoded":
        return ERROR_PING.format("Invalid content type.")

    domain = urlparse(url).netloc

    if valid_domains and domain not in valid_domains:
        return ERROR_PING.format("Invalid domain.")

    return SUCCESSFUL_PING

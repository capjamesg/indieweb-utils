from urllib import parse as url_parse

class InvalidURL(Exception):
    """
    URL cannot be parsed to retrieve a summary.
    """
    pass

def _get_path_sections(path: str) -> list:
    """
    Get a list of all the items in a URL path.
    """

    path_sections = path.split("/")

    # remove blank values from list
    path_sections.remove("")

    if len(path_sections) == 0:
        return []

    return path_sections


def _github_auto_summary(path: str) -> str:
    """
    Retrieve the summary of a GitHub URL.
    """

    path_sections = _get_path_sections(path)

    project_name = path_sections[1]

    if len(path_sections) > 2:
        page_type = path_sections[2]

        if page_type == "issues":
            return "A comment on issue " + path_sections[3] + " in the " + project_name + " repository."
        elif page_type == "pull":
            return "A comment on pull request " + path_sections[3] + " in the " + project_name + " repository."

    return "A comment on GitHub in the " + project_name + " repository."


def _social_network_url_summaries(domain: str, path: str) -> str:
    """
    Retrieve the summary of a social network URL.
    """

    path_sections = _get_path_sections(path)

    if domain in ("eventbrite.com", "eventbrite.co.uk"):
        return "An Eventbrite event."
    elif domain == "upcoming.com":
        return "An Upcoming event."
    elif domain == "calagator.com":
        return "A Calagator event."
    elif domain == "events.indieweb.org":
        return "An IndieWeb event."
    elif domain == "twitter.com":
        return "A Tweet from @" + path_sections[0] + "."

    return ""


def get_url_summary(url: str, custom_mappings: dict = {}) -> str:
    """
    Retrieve a sentence summarising the contents of a URL, based on the auto_url_summary function in CASSIS.

    :refs: https://indieweb.org/auto-url-summary:
    :refs: https://github.com/tantek/cassis/blob/master/cassis-lab.php#L52:

    :param url: The URL whose summary you want to retrieve.
    :type url: str

    :return: The summary of the URL.
    :rtype: str

    .. code-block:: python

        import indieweb_utils

        url_summary = indieweb_utils.get_url_summary(
            "https://github.com/capjamesg/indieweb-utils/issues/56"
        )

        print(url_summary)

    :raises InvalidURL: The URL cannot be parsed to retrieve a summary.
    """

    parsed_url = url_parse.urlsplit(url)

    domain = parsed_url.netloc
    path = parsed_url.path

    if domain == "":
        raise InvalidURL("The URL cannot be parsed to retrieve a summary.")

    # remove www from beginning of a domain
    domain = domain.lstrip("www.")

    if domain == "github.com":
        return _github_auto_summary(path)

    social_network_response = _social_network_url_summaries(domain, path)

    if social_network_response != "":
        return social_network_response

    if custom_mappings.get(domain) is not None:
        return custom_mappings.get(domain)

    return "A post by " + domain + "."

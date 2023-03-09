from urllib import parse as url_parse


def canonicalize_url(url: str, domain: str = "", full_url: str = "", protocol: str = "https") -> str:
    """
    Return a canonical URL for the given URL.

    :param url: The URL to canonicalize.
    :type url: str
    :param domain: The domain to use for the canonical URL.
    :type domain: str
    :param full_url: Optional full URL to use for the canonical URL.
    :type full_url: str or None
    :param protocol: Optional protocol to use for the canonical URL.
    :type protocol: str or None
    :return: The canonical URL.
    :rtype: str

    .. code-block:: python

        import indieweb_utils

        url = "/contact"
        domain = "jamesg.blog"
        protocol = "https"

        endpoints = indieweb_utils.canonicalize_url(
            url, domain, protocol=protocol
        )

        print(webmention_endpoint) # https://jamesg.blog/contact/
    """

    if _is_http_url(url):
        domain = url_parse.urlsplit(url).netloc

        # remove port from domain

        domain = domain.split(":")[0]

        protocol = url_parse.urlsplit(url).scheme

        return protocol + "://" + domain + "/" + "/".join(url.split("/")[3:])

    current_protocol = url_parse.urlsplit(url).scheme

    # this will preserve links like irc:// and mailto:
    if current_protocol:
        return url

    if ":" in domain:
        text_before_port = domain.split(":")[0]

        text_after_port = domain.split(":")[1].split("/")[0]

        domain = text_before_port + "/" + text_after_port

    final_result = ""

    if url.startswith("//"):
        final_result = protocol + ":" + domain.strip() + "/" + url
    elif url.startswith("/"):
        final_result = protocol + "://" + domain.strip() + "/" + url
    elif url.startswith("./"):
        final_result = full_url + url[1:]
    elif url.startswith("../"):
        final_result = protocol + "://" + domain.strip() + "/" + url[3:]
    else:
        final_result = protocol + "://" + url

    # replace ../ throughout url

    url_after_replacing_dots = ""

    to_check = final_result.replace(domain, "").replace(protocol + "://", "")

    for url_item in to_check.split("/"):
        if url_item == "..":
            # directory before ../
            directory = url_after_replacing_dots.split("/")[-1]
            url_after_replacing_dots = url_after_replacing_dots.replace(directory, "")
        else:
            url_after_replacing_dots += "/" + url_item

    url_after_replacing_dots = url_after_replacing_dots.lstrip("/")

    # replace ./ throughout url

    url_after_replacing_dots = url_after_replacing_dots.replace("./", "/")

    final_url = protocol + "://" + domain + "/" + url_after_replacing_dots.lstrip("/")

    return final_url


def _is_http_url(url: str) -> bool:
    """
    Determine if URL is http or not
    """
    return url_parse.urlsplit(url).scheme in ["http", "https"]


def remove_tracking_params(url: str, custom_params: list) -> str:
    """
    Remove all UTM tracking parameters from a URL.

    :param url: The URL to remove tracking parameters from.
    :type url: str
    :param custom_params: A list of custom parameters to remove.
    :type custom_params: list
    :return: The URL without tracking parameters.
    :rtype: str

    Example:

    .. code-block:: python

        import indieweb_utils

        url = "https://jamesg.blog/indieweb/?utm_source=twitter&utm_medium=social&utm_campaign=webmention"

        url_without_tracking = indieweb_utils.remove_tracking_params(url)

        print(url_without_tracking) # https://jamesg.blog/indieweb/
    """

    parsed_url = url_parse.urlparse(url.lower())

    query = url_parse.parse_qs(parsed_url.query)

    for key in query.keys():
        if key.startswith("utm_") or key.startswith(custom_params):
            del query[key]

    new_query = url_parse.urlencode(query, doseq=True)

    new_url = url_parse.urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment)
    )

    return new_url


def is_site_url(url: str, domain: str) -> bool:
    """
    Determine if a URL is a site URL.

    :param url: The URL to check.
    :type url: str
    :param domain: The domain to check against.
    :type domain: str
    :return: Whether or not the URL is a site URL.
    :rtype: bool

    :raises ValueError: If the URL does not include a scheme.

    Example:

    .. code-block:: python

        import indieweb_utils

        url = "https://jamesg.blog/indieweb/"
        domain = "jamesg.blog"

        is_site_url = indieweb_utils.is_site_url(url, domain)

        print(is_site_url) # True
    """

    parsed_url = url_parse.urlparse(url)

    if parsed_url.scheme == "":
        raise ValueError("URL must include a scheme")

    if parsed_url.netloc == "":
        return False

    return url_parse.urlsplit(url).netloc == domain


def slugify(url: str, remove_extension: bool = False, allowed_chars: list = ["-", "/", "_", "."]) -> str:
    """
    Turn a URL into a slug. Only alphanumeric characters, periods, dashes, and underscores are allowed in the resulting slug,
    unless an allowed_chars list is provided.

    :param url: The URL to slugify.
    :type url: str
    :param remove_extension: Whether or not to remove the file extension from the slug.
    :type remove_extension: bool
    :param allowed_chars: A list of allowed characters.
    :type allowed_chars: list
    :return: A slugified URL.

    Example:

        from indieweb.utils import slugify

        slugify("https://jamesg.blog/indieweb.html", True) # https://jamesg.blog/indieweb/
        slugify("indieweb.html", True) # /indieweb/
    """
    if _is_http_url(url):
        parsed_url = url_parse.urlparse(url)
        full_url = url_parse.unquote(parsed_url.path)
    else:
        full_url = url_parse.unquote(url)

    # replace all space / with -
    full_url = full_url.replace(" /", "/test.md")

    # get file extension
    extension = full_url.split(".")[-1]

    if remove_extension and extension:
        # remove file extension
        full_url = full_url.replace(f".{extension}", "/")

    path = "".join([char for char in full_url.replace(" ", "-") if char.isalnum() or char in allowed_chars])

    if url.startswith("http"):
        # recompose url and replace
        return parsed_url._replace(path=path).geturl()

    path = path.lstrip("/")
    path = "/" + path

    return path

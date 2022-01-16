from urllib import parse as url_parse


def canonicalize_url(url, domain, full_url=None, protocol="https"):
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
    """

    if url.startswith("http://") or url.startswith("https://"):
        domain = url_parse.urlsplit(url).netloc

        # remove port from domain

        domain = domain.split(":")[0]

        protocol = url_parse.urlsplit(url).scheme

        return protocol + "://" + domain + "/" + "/".join(url.split("/")[3:])

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

from dataclasses import dataclass

import mf2py


@dataclass
class ApplicationInfo:
    name: str
    logo: str
    url: str
    summary: str


class HAppNotFound(Exception):
    pass


def get_h_app_item(web_page: str) -> ApplicationInfo:
    """
    Get the h-app item from the web page.

    :param web_page: The web page to parse.
    :type web_page: str
    :param client_id: The client id of your application.
    :type client_id: str
    :return: The h-app item.
    :rtype: ApplicationInfo

    Example:

    .. code-block:: python

        import indieweb_utils

        app_url = "https://quill.p3k.io/"
        client_id = "https://quill.p3k.io/"

        h_app_item = indieweb_utils.get_h_app_item(
            app_url, client_id
        )

        print(h_app_item.name) # Quill

    :raises HAppNotFound: Raised if no mf2 h-app data was found on the specified page.
    """

    parsed_document = mf2py.parse(doc=web_page)

    if not parsed_document:
        raise HAppNotFound("No h-app mf2 data was found on the specified page.")

    for item in parsed_document["items"]:
        if item.get("type") and item.get("type")[0] == "h-app":
            values = ["name", "logo", "url", "summary"]

            value_dict = {}

            for v in values:
                value_dict[v] = item["properties"].get(v)

                if value_dict[v] is None:
                    value_dict[v] = ""
                else:
                    value_dict[v] = value_dict[v][0]

            return ApplicationInfo(**value_dict)

    raise HAppNotFound("No h-app mf2 data was found on the specified page.")

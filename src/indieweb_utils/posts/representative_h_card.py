from dataclasses import dataclass
from typing import Any, Dict

import mf2py


class RepresentativeHCardParsingError(Exception):
    pass


@dataclass
class RepresentativeHCard:
    # TODO: Fill this out with a full h-card object
    pass


def get_representative_h_card(url: str) -> Dict[str, Any]:
    """
    Get the representative h-card on a page per the Representative h-card Parsing algorithm.

    refs: https://microformats.org/wiki/representative-h-card-parsing

    :url: The url to parse.
    :type url: str
    :return: The representative h-card.
    :rtype: dict
    """
    mf2_data = mf2py.parse(url=url)

    if not mf2_data:
        raise RepresentativeHCardParsingError("No mf2 data found.")

    if not mf2_data.get("items"):
        raise RepresentativeHCardParsingError("No items found.")

    h_cards = [card for card in mf2_data["items"] if card.get("type") and card.get("type")[0] == "h-card"]

    rel_me_links = mf2_data["rels"].get("me", [])

    for h_card in h_cards:
        if h_card.get("uid", "") == url and h_card.get("url", "") == url:
            return h_card

        if h_card.get("url", "") in rel_me_links:
            return h_card

    if len(h_cards) == 1:
        return h_card

    return {}

from dataclasses import dataclass

import requests

from bs4 import BeautifulSoup


class ProfileError(Exception):
    pass


@dataclass
class Profile:
    name: str
    photo: str
    url: str
    email: str


def get_profile(
        me: str
    ) -> Profile:

    try:
        me_profile = requests.get(me)
    except:
        raise ProfileError("Request to retrieve profile URL did not return a valid response.")

    if not me_profile:
        return Profile(
            name="",
            photo="",
            url="",
            email=""
        )

    profile_item = BeautifulSoup(me_profile.text, "html.parser")
    h_card = profile_item.select(".h-card")

    if not h_card:
        return Profile(
            name="",
            photo="",
            url="",
            email=""
        )
            
    h_card = h_card[0]
    name = h_card.select(".p-name")
    photo = h_card.select(".u-photo")
    url = h_card.select(".u-url")
    email = h_card.select(".u-email")

    profile = {}

    if name and name[0].text.strip() != "":
        profile["name"] = name[0].text
    else:
        profile["name"] = me

    if photo:
        profile["photo"] = photo[0].get("src")
    
    if url and url[0].get("href").strip() != "":
        profile["url"] = url[0].get("href")
    else:
        profile["url"] = me

    if email:
        profile["email"] = email[0].text.replace("mailto:", "")
    else:
        profile["email"] = None

    return Profile(
        name=profile["name"],
        photo=profile["photo"],
        url=profile["url"],
        email=profile["email"]
    )
    
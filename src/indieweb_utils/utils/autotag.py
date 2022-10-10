import re
from typing import List


def _match_tag(tag_prefix: str, match: str, user_tags: List[str]) -> str:
    """
    Match a tag and return a link to the tag page.

    :param tag_prefix: The prefix to append to the tag.
    :type tag_prefix: str
    :param match: The match to process.
    :type match: str
    :param user_tags: A list of tags that a user supports on their website.
    :type user_tags: List[str]
    :return: The processed match.
    :rtype: str
    """
    tag = match[1:]
    if len(user_tags) > 0 and tag in user_tags:
        return f"<a href='{tag_prefix}{tag}'>#{tag}</a>"
    else:
        return match


def _match_person_tag(people: dict, match: str) -> str:
    """
    A person tag and return a link to their profile.

    :param people: A dictionary of names to which a person tag can be matched.
    :type people: dict
    :param match: The match to process.
    :type match: str
    :return: The processed match.
    :rtype: str
    """
    person = match[1:]
    if people.get(person):
        return f"<a href='{people[person][1]}'>{people[person][0]}</a>"
    else:
        return match


def autolink_tags(text: str, tag_prefix: str, people: dict, tags: List[str] = None) -> str:
    """
    Replace hashtags (#) and person tags (@) with links to the respective tag page and profile URL.

    :param text: The text to process.
    :type text: str
    :param tag_prefix: The prefic to append to identified tags.
    :type tag_prefix: str
    :param people: A dictionary of people to link to.
    :type people: dict
    :param tags: A list of tags to link to (optional).
    :type tags: List[str]
    :return: The processed text.
    :rtype: str

    Example:

    .. code-block:: python

        import indieweb_utils

        note = "I am working on a new #muffin #recipe with @jane"

        # tag to use, name of person, domain of person
        people = { "jane": ("Jane Doe", "https://jane.example.com") }

        note_with_tags = indieweb_utils.autolink_tags(note, "/tag/", people, tags=["muffin", "recipe"])

    """

    if tags is None:
        tags = []

    tag_list = list(set(tags))

    text = re.sub(r"#(\w+)", lambda match: _match_tag(tag_prefix, match.group(), tag_list), text)
    text = re.sub(r"@(\w+)", lambda match: _match_person_tag(people, match.group()), text)

    return text

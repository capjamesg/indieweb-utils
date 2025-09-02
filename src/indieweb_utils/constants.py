import re

USER_AGENT = "indieweb-utils"
ACTIVITYPUB_USERNAME_REGEX = re.compile(r"^@([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)$")
BLUESKY_USERNAME_REGEX = re.compile(r"^@([a-zA-Z0-9._-]+)")
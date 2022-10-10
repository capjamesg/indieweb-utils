URL_SUMMARY_TEMPLATES = {
    "github.com": [
        (
            r"(?P<user>.+)/(?P<project>.+)/issues/(?P<issue>\d+)",
            "A comment on issue #{issue} in the {project} GitHub repository",
        ),
        (
            r"(?P<user>.+)/(?P<project>.+)/pull/(?P<pull>\d+)",
            "A comment on pull request #{pull} in the {project} GitHub repository",
        ),
        (
            r"(?P<user>.+)/(?P<project>.+)",
            "A comment on the {project} GitHub repository",
        ),
    ],
    "twitter.com": [
        (
            r"(?P<user>[^/]+)",
            "A tweet by @{user}",
        ),
    ],
    "upcoming.com": [
        (
            "",
            "An event on Upcoming",
        )
    ],
    "eventbrite.com": [
        (
            "",
            "An event on Eventbrite",
        )
    ],
    "eventbrite.co.uk": [
        (
            "",
            "An event on Eventbrite",
        )
    ],
    "calagator.com": [
        (
            "",
            "An event on Calagator",
        )
    ],
    "events.indieweb.org": [
        (
            "",
            "An event on IndieWeb events",
        )
    ],
    "indieweb.org": [
        (
            r"(?P<page>.+)",
            "The /{page} page on the IndieWeb wiki",
        )
    ],
}

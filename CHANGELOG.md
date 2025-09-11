# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.10.0] - 2025-09-11

## Added

- You can now set the user agent with which IndieWeb Utils will make requests. To do so, import the library, then, immediately after, set `indieweb_utils.USER_AGENT = 'your-user-agent'`.
- The `get_web_feed_url()` lets you match a URL against several services that offer RSS feeds that may not be automatically discoverable. If a URL matches a pattern, the corresponding feed URL is returned. The computed feed URL is not validated by the function. You should write code to make sure the feed exists.
- `signed_web_bot_auth_request()` lets you make a signed HTTP request using the [Web Bot Auth](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/web-bot-auth/) system.
- `check_if_feed_is_bsky()` transforms `https://bsky.app/profile/username` into `@username`.
- The `generate_token()` IndieAuth method now generates a JWT with `exp` and `iat` values.
- The `redeem_code()` method nowreturns a JWT access token with `exp` and `iat` values.
- `discover_edit_links()` lets you discover rel=edit links per the [rel=edit specification](https://microformats.org/wiki/rel-edit).
- `canonicalize_url()` now depends more on the `urllib` library. This should reduce the number of edge cases in URL canonicalization.
- [python-jose](https://pypi.org/project/python-jose/) is now used to generate JWT tokens. This allows tokens to be both signed and encrypted.

## Bug Fixes

- `application/jf2feed+json` feeds can now be discovered through `discover_web_page_feeds`.
- `get_valid_relmeauth_links()` can now return `mailto:` links.
- The `get_reply_context()` function no longer returns an error if the microformat for a featured image or a video is processed as a dictionary rather than a list. This was an internal bug caused by missing logic to validate the type of object in those microformats.
- `send_webmention` now returns the `summary` result from a Webmention endpoint if the endpoint returns a JSON response with a `summary` value.

## Breaking Changes

- `validate_authorization_response()` now requires a code challenge as an argument. The function previously generated a new code challenge, which was not the correct behaviour.
- `redeem_code()` now decodes code challenges as UTF-8 and applies the required `.rstrip(b"=")` transformation. If you are using IndieWeb Utils both to support a client and a server, both your clients and server will need to be updated to make sure they are all using the same code redemption logic.

## Removed Functions

- The `_generate_tweet_reply_context()` internal function, used to generate reply contexts from Twitter, has now been removed. This was previously used by `get_reply_context()`. As part of this change, `get_reply_context()` no longer accepts the `twitter_bearer_token` argument.

# [0.9.0] - 2024-06-24

## What's Changed

* Add support for polling feeds and retrieving their contents as JSON Feed data with `indieweb_utils.retrieve_feed_contents`.

# [0.8.0] - 2023-03-09

### Added

#### Development

- `add_footnote_links()` replaces [n] and [^n] links with HTML `<a>` tags that link to each other.
- `reduce_image_size()` abstracts the PIL resize feature to provide an easy utility for image resizing.
- `Paginator` class creates paginated list with generators to navigate through each page in the list.
- `process_salmention()` compares stored and live version of a page to find new and deleted responses. Optionally, Webmentions can be sent to all response URLs that are present on both pages.
- `remove_tracking_parameters()` removes UTM parameters and optionally custom provided parameters from a URL.
- `is_site_url()` checks if a URL is on a specified domain.
- `slugify()` removes all characters in a URL that are not alphanumerics, a period, a dash, or an underscore.
- Added types for Trackback code that did not have complete typing.

# [0.7.2] - 2023-03-02

[Released without changelog notes. Requires backfilling.]

# [0.7.1] - 2023-03-02

### Added

#### Development

- `process_trackback` function to process a Trackback request and return a response.
- `SUCCESSFUL_PING` and `ERROR_PING` constants to use in the `process_trackback` function and for use in custom Trackback validation logic.

### Fixed

- Fixed import statements for `rsd_trackback_discovery`, `discover_trackback_url`, and `send_trackback` functions so that they can all be imported from the top-level of the library.

# [0.7.0] - 2023-03-01

### Added

#### Development

- `rsd_discovery` function to find values associated with keys in a [Really Simple Discovery](https://en.wikipedia.org/wiki/Really_Simple_Discovery) file.
- `send_trackback` function to send a Trackback to a specified URL.
- `discover_trackback_url` function to discover the Trackback endpoint for a specified URL.

# [0.6.2] - 2022-10-21

### Development

- `send_webmention` now looks for a message in a `message` key and has a fallback if one cannot be found. This information is returned in the `title` and `description` values in the Webmention response. The message will be blank if one cannot be found.

### Fixed

- Fixed a bug where the `send_webmention` function raised an error when trying to retrieve a message from an endpoint.

## [0.6.1] - 2022-10-21

No change. Changes moved to 0.6.2.

## [0.6.0] - 2022-10-18

### Added

#### Development

- Support for sending private Webmentions in the `send_webmention` function.
- New docstrings documenting parameters used to send a private webmention using the `send_webmention` function.
- Support for validating private Webmentions in the `validate_webmention` function.
- New docstrings documenting parameters used to validate a private webmention with the `validate_webmention` function.
- `validate_webmention` returns the text and a parsed Beautiful Soup tree of the source of a validated Webmention in the `WebmentionCheckResponse` return object.

#### Functions

- `discover_indieauth_endpoints` function to discover endpoints mentioned in the [IndieAuth spec](https://indieauth.spec.indieweb.org/) and ticket endpoints used in [TicketAuth](https://indieweb.org/IndieAuth_Ticket_Auth), a proposed extension to IndieAuth.

### Tests

- Added tests for `discover_indieauth_endpoints` function.


## [0.5.0] - 2022-10-13

### Added

- `get_reply_context` now performs discovery on `property` and `name` values for og:image, twitter:image:src, description, og:description, and twitter:description tags.

### Tests

- Added new tests for the `get_reply_context` function.
- Added `responses.activate` decorators to remaining tests that did not already have this decorator present. This ensures all tests run on the contents of local files rather than making network requests to get data from a page.

### Fixed

- `get_reply_context` would use a h-entry even if the h-entry only provided a URL and no other content.
- `indieweb_utils.SCOPE_DEFINITIONS` can now be imported into a project. This previously returned an `ImportError` exception.


## [0.4.0] - 2022-10-11

### Added

#### Development

- Documentation for the `discover_endpoints` function.
- The `indieauth_callback_handler` function returns the JSON response from an IndieAuth endpoint represented as a dictionary instead of a blank dictionary.
- The `discover_endpoints` docstring contains an example about Microsub and an updated common values list. This is because we recommend use of the `discover_webmention_endpoint` function for Webmention endpoint discovery.

#### Functions

- `get_reply_urls` to retrieve all of the URLs to which a specified page is replying.
- `get_page_name` to find the name of a page per the IndieWeb [Page Name Discovery](https://indieweb.org/page-name-discovery) algorithm.
- `get_syndicated_copies` to retrieve all of the URLs to which a specified page has been syndicated.

#### Tests

- Added test cases for:
    - `get_reply_urls`
    - `get_page_name`
    - `get_syndicated_copies`
- Updated test cases for `get_reply_context` were to look for `description` values where appropriate.

### Fixed

- The `indieauth_callback_handler` function no longer raises a JSON error during the `_validate_indieauth_response` function call.
- The `get_reply_context` function now returns a description based on the first two sentences of the e-content of a specified page if a summary cannot be found when analysing a h-entry.
- The `get_reply_context` function returns a string `summary` value instead of a dictionary or a list.
- `get_reply_context` now looks at `og:description` and `twitter:description` meta tags for a description if a `description` value cannot be found. This happens when analysing a page that does not contain a h-entry.

## [0.3.1] - 2022-10-10

Fixed import issue in `setup.cfg` so PyPi can discover the README for indieweb-utils.

## [0.3.0] - 2022-10-10

### Added

#### Development

- Provide docstrings for all functions in the library that did not have a docstring.
- Fix docstring rendering issues with library documentation so that all docstrings show up on [Read the Docs](https://indieweb-utils.readthedocs.io/en/latest/).
- Add `:raises:` statements to docstrings to document existing
- Add code examples to docstrings and remove redundant examples from RS documentation.
- Add a [SECURITY.md](https://github.com/capjamesg/indieweb-utils/blob/main/SECURITY.md) policy.
- Split up documentation into more sections to enhance one's ability to navigate the documentation.

#### Functions

- `discover_h_feed()` function to discover the representative h-feed on a page.
- `get_valid_relmeauth_links()` function to find both one-way and bi-directional rel=me links on a web page.
- `get_representative_h_card()` function to get the [representative h-card](https://microformats.org/wiki/representative-h-card-parsing) associated with a web page.
- `get_url_summary()` function to generate a summary from a URL, based on the experimental [CASSIS auto_url_summary PHP function](https://indieweb.org/auto-url-summary#Open_Source).
    - This function provides examples for GitHub, Twitter, Upcoming, Eventbrite (.com and .co.uk), Calagator, [IndieWeb Events](https://events.indieweb.org), and the [IndieWeb wiki](https://indieweb.org).
- `autolink_tags()` function to replace hashtags (#) with relevant tag pages and person tags (@) with the names and domains of people tagged.
- Create internal helper functions:
    - `get_parsed_mf2_data()` to retrieve microformats2 data from a page given a parsed mf2py.Parse object, a HTML string, and a URL.
    - `get_soup()` to retrieve a BeautifulSoup object from a provided HTML string and URL.

#### Tests

- Added test cases for:
    - `discover_h_feed()`
    - `get_representative_h_card()`
    - `get_valid_relmeauth_links()`
    - `get_url_summary()`
    - `autolink_tags()`

### Changed

- Support importing IndieAuth functions directly from `indieweb_utils` without having to use `indieweb_utils.indieauth.`.
- Simplify `get_h_app_item()` logic.
- Raise `HAppNotFound` exception when `get_h_app_item()` cannot identify a h-app microformat.
- Renamed `_discover_endpoints` to `discover_endpoints`.
- `discover_endpoints` can raise a `requests.exceptions.RequestException` if there was an error making a request to retrieve an endpoint.
- `discover_webmention_endpoint()` can now raise LocalhostEndpointFound, TargetNotProvided, UnacceptableIPAddress, and WebmentionEndpointNotFound exceptions when there is an issue validating a webmention.
- `send_webmention()` can now raise MissingSourceError, MissingTargetError, UnsupportedProtocolError, TargetIsNotApprovedDomain, GenericWebmentionError, and CouldNotConnectToWebmentionEndpoint if there was an issue sending a webmention.
- `send_webmention()` now returns the HTTP status code and headers of a successful webmention.
- `get_post_type()` raises an `PostTypeFormattingError` exception if an invalid `custom_properties` tuple is provided.
- `get_reply_context()` raises an `ReplyContextRetrievalError` if there was an error retrieving context for a URL. This function also raises an `UnsupportedScheme` error if a URL does not use either HTTP or HTTPS.
- `validate_webmention()` can raise WebmentionIsGone or WebmentionValidationError exceptions if there was an error validating a webmention.
- `canonicalize_url()` returns the exact URL passed in if the URL contains a protocol that is not HTTP or HTTPS.

## [0.2.0] - 2022-02-15

### Added

- Constants that document different scopes one may want to use in an IndieAuth server.
- Test cases for all main library functions.
- Web page feed discovery function now looks for more MIME types by default.
- New exceptions to throw various errors.
- Add X-Pingback support to feed parsing.
- Use urllib to retrieve domain names, protocols, and paths throughout the library.

#### Development

- Use tox, black, isort, flake8, and mypy to control quality of code.
- Type hints are used for all functions.
- New documentation has been added for all functions in the library.
- New code snippet examples to function docstrings.

#### Functions

- `get_h_app_item` function to retrieve a h-app object from a web page.
- `validate_authorization_response` function to validate an IndieAuth authorization response.
- `_verify_decoded_code` function that verifies a decoded code in an IndieAuth request.
- `generate_auth_token` function to generate an authentication token as part of an IndieAuth server.
- `redeem_code` function to handle token redemption in an IndieAuth server.
- `send_webmention` function to send a webmention.
- `validate_webmention` to validate a webmention according to the Webmention specification. Vouch support is implemented as an optional feature to use during the validation process.
- `get_profile` function to retrieve profile information from a h-card on a URL from a URL.

### Changed

- Functions now return documented objects instead of arbitrary dictionaries.
- Exceptions are now thrown instead of returning None values or empty dictionaries.
- Fixed various bugs in the reply context function.
- Refactored test cases.
- Code has been formatted using black and isort for readability and adherence to PEP 8.

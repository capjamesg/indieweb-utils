Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.5.0] - 2022-10-13
--------------------

Added
~~~~~

-  ``get_reply_context`` now performs discovery on ``property`` and
   ``name`` values for og:image, twitter:image:src, description,
   og:description, and twitter:description tags.

Tests
~~~~~

-  Added new tests for the ``get_reply_context`` function.
-  Added ``responses.activate`` decorators to remaining tests that did
   not already have this decorator present. This ensures all tests run
   on the contents of local files rather than making network requests to
   get data from a page.

Fixed
~~~~~

-  ``get_reply_context`` would use a h-entry even if the h-entry only
   provided a URL and no other content.
-  ``indieweb_utils.SCOPE_DEFINITIONS`` can now be imported into a
   project. This previously returned an ``ImportError`` exception.

.. _section-1:

[0.4.0] - 2022-10-11
--------------------

.. _added-1:

Added
~~~~~

Development
^^^^^^^^^^^

-  Documentation for the ``discover_endpoints`` function.
-  The ``indieauth_callback_handler`` function returns the JSON response
   from an IndieAuth endpoint represented as a dictionary instead of a
   blank dictionary.
-  The ``discover_endpoints`` docstring contains an example about
   Microsub and an updated common values list. This is because we
   recommend use of the ``discover_webmention_endpoint`` function for
   Webmention endpoint discovery.

Functions
^^^^^^^^^

-  ``get_reply_urls`` to retrieve all of the URLs to which a specified
   page is replying.
-  ``get_page_name`` to find the name of a page per the IndieWeb `Page
   Name Discovery <https://indieweb.org/page-name-discovery>`__
   algorithm.
-  ``get_syndicated_copies`` to retrieve all of the URLs to which a
   specified page has been syndicated.

.. _tests-1:

Tests
^^^^^

-  Added test cases for:

   -  ``get_reply_urls``
   -  ``get_page_name``
   -  ``get_syndicated_copies``

-  Updated test cases for ``get_reply_context`` were to look for
   ``description`` values where appropriate.

.. _fixed-1:

Fixed
~~~~~

-  The ``indieauth_callback_handler`` function no longer raises a JSON
   error during the ``_validate_indieauth_response`` function call.
-  The ``get_reply_context`` function now returns a description based on
   the first two sentences of the e-content of a specified page if a
   summary cannot be found when analysing a h-entry.
-  The ``get_reply_context`` function returns a string ``summary`` value
   instead of a dictionary or a list.
-  ``get_reply_context`` now looks at ``og:description`` and
   ``twitter:description`` meta tags for a description if a
   ``description`` value cannot be found. This happens when analysing a
   page that does not contain a h-entry.

.. _section-2:

[0.3.1] - 2022-10-10
--------------------

Fixed import issue in ``setup.cfg`` so PyPi can discover the README for
indieweb-utils.

.. _section-3:

[0.3.0] - 2022-10-10
--------------------

.. _added-2:

Added
~~~~~

.. _development-1:

Development
^^^^^^^^^^^

-  Provide docstrings for all functions in the library that did not have
   a docstring.
-  Fix docstring rendering issues with library documentation so that all
   docstrings show up on `Read the
   Docs <https://indieweb-utils.readthedocs.io/en/latest/>`__.
-  Add ``:raises:`` statements to docstrings to document existing
-  Add code examples to docstrings and remove redundant examples from RS
   documentation.
-  Add a
   `SECURITY.md <https://github.com/capjamesg/indieweb-utils/blob/main/SECURITY.md>`__
   policy.
-  Split up documentation into more sections to enhance one’s ability to
   navigate the documentation.

.. _functions-1:

Functions
^^^^^^^^^

-  ``discover_h_feed()`` function to discover the representative h-feed
   on a page.
-  ``get_valid_relmeauth_links()`` function to find both one-way and
   bi-directional rel=me links on a web page.
-  ``get_representative_h_card()`` function to get the `representative
   h-card <https://microformats.org/wiki/representative-h-card-parsing>`__
   associated with a web page.
-  ``get_url_summary()`` function to generate a summary from a URL,
   based on the experimental `CASSIS auto_url_summary PHP
   function <https://indieweb.org/auto-url-summary#Open_Source>`__.

   -  This function provides examples for GitHub, Twitter, Upcoming,
      Eventbrite (.com and .co.uk), Calagator, `IndieWeb
      Events <https://events.indieweb.org>`__, and the `IndieWeb
      wiki <https://indieweb.org>`__.

-  ``autolink_tags()`` function to replace hashtags (#) with relevant
   tag pages and person tags (@) with the names and domains of people
   tagged.
-  Create internal helper functions:

   -  ``get_parsed_mf2_data()`` to retrieve microformats2 data from a
      page given a parsed mf2py.Parse object, a HTML string, and a URL.
   -  ``get_soup()`` to retrieve a BeautifulSoup object from a provided
      HTML string and URL.

.. _tests-2:

Tests
^^^^^

-  Added test cases for:

   -  ``discover_h_feed()``
   -  ``get_representative_h_card()``
   -  ``get_valid_relmeauth_links()``
   -  ``get_url_summary()``
   -  ``autolink_tags()``

Changed
~~~~~~~

-  Support importing IndieAuth functions directly from
   ``indieweb_utils`` without having to use
   ``indieweb_utils.indieauth.``.
-  Simplify ``get_h_app_item()`` logic.
-  Raise ``HAppNotFound`` exception when ``get_h_app_item()`` cannot
   identify a h-app microformat.
-  Renamed ``_discover_endpoints`` to ``discover_endpoints``.
-  ``discover_endpoints`` can raise a
   ``requests.exceptions.RequestException`` if there was an error making
   a request to retrieve an endpoint.
-  ``discover_webmention_endpoint()`` can now raise
   LocalhostEndpointFound, TargetNotProvided, UnacceptableIPAddress, and
   WebmentionEndpointNotFound exceptions when there is an issue
   validating a webmention.
-  ``send_webmention()`` can now raise MissingSourceError,
   MissingTargetError, UnsupportedProtocolError,
   TargetIsNotApprovedDomain, GenericWebmentionError, and
   CouldNotConnectToWebmentionEndpoint if there was an issue sending a
   webmention.
-  ``send_webmention()`` now returns the HTTP status code and headers of
   a successful webmention.
-  ``get_post_type()`` raises an ``PostTypeFormattingError`` exception
   if an invalid ``custom_properties`` tuple is provided.
-  ``get_reply_context()`` raises an ``ReplyContextRetrievalError`` if
   there was an error retrieving context for a URL. This function also
   raises an ``UnsupportedScheme`` error if a URL does not use either
   HTTP or HTTPS.
-  ``validate_webmention()`` can raise WebmentionIsGone or
   WebmentionValidationError exceptions if there was an error validating
   a webmention.
-  ``canonicalize_url()`` returns the exact URL passed in if the URL
   contains a protocol that is not HTTP or HTTPS.

.. _section-4:

[0.2.0] - 2022-02-15
--------------------

.. _added-3:

Added
~~~~~

-  Constants that document different scopes one may want to use in an
   IndieAuth server.
-  Test cases for all main library functions.
-  Web page feed discovery function now looks for more MIME types by
   default.
-  New exceptions to throw various errors.
-  Add X-Pingback support to feed parsing.
-  Use urllib to retrieve domain names, protocols, and paths throughout
   the library.

.. _development-2:

Development
^^^^^^^^^^^

-  Use tox, black, isort, flake8, and mypy to control quality of code.
-  Type hints are used for all functions.
-  New documentation has been added for all functions in the library.
-  New code snippet examples to function docstrings.

.. _functions-2:

Functions
^^^^^^^^^

-  ``get_h_app_item`` function to retrieve a h-app object from a web
   page.
-  ``validate_authorization_response`` function to validate an IndieAuth
   authorization response.
-  ``_verify_decoded_code`` function that verifies a decoded code in an
   IndieAuth request.
-  ``generate_auth_token`` function to generate an authentication token
   as part of an IndieAuth server.
-  ``redeem_code`` function to handle token redemption in an IndieAuth
   server.
-  ``send_webmention`` function to send a webmention.
-  ``validate_webmention`` to validate a webmention according to the
   Webmention specification. Vouch support is implemented as an optional
   feature to use during the validation process.
-  ``get_profile`` function to retrieve profile information from a
   h-card on a URL from a URL.

.. _changed-1:

Changed
~~~~~~~

-  Functions now return documented objects instead of arbitrary
   dictionaries.
-  Exceptions are now thrown instead of returning None values or empty
   dictionaries.
-  Fixed various bugs in the reply context function.
-  Refactored test cases.
-  Code has been formatted using black and isort for readability and
   adherence to PEP 8.

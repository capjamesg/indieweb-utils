Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.2.0] - 2022-02-15
--------------------

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

Development
^^^^^^^^^^^

-  Use tox, black, isort, flake8, and mypy to control quality of code.
-  Type hints are used for all functions.
-  New documentation has been added for all functions in the library.
-  New code snippet examples to function docstrings.

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

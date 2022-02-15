# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2022-02-15

### Added

- Use tox, black, isort, flake8, and mypy to control quality of code.
- New function that verifies whether a webmention is valid.
- Constants that document different scopes one may want to use in an IndieAuth server.
- New function that retrieve a h-app object from a web page.
- New function that validates an IndieAuth authorization response.
- New function that verifies a decoded code in an IndieAuth request.
- New function to generate an authentication token as part of an IndieAuth server.
- New function to handle token redemption in an IndieAuth server.
- Test cases for all main library functions.
- Web page feed discovery function now looks for more MIME types by default.
- Type hints are used for all functions.
- New documentation has been added for all functions in the library.
- Code snippet examples to function docstrings.
- New exceptions to throw various errors.
- Add X-Pingback support to feed parsing.
- Use urllib to retrieve domain names, protocols, and paths throughout the library.
- New function to send a webmention.

### Changed

- Functions now return documented objects instead of arbitrary dictionaries.
- Exceptions are now thrown instead of returning None values or empty dictionaries.
- Fixed various bugs in the reply context function.
- Refactored test cases.
- Code has been formatted using black and isort for readability and adherence to PEP 8.
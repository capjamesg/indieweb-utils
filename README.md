# Python indieweb-utils Library

[![Documentation Status](https://readthedocs.org/projects/indieweb-utils/badge/?version=latest)](https://indieweb-utils.readthedocs.io/en/latest/?badge=latest)
[![image](https://badge.fury.io/py/indieweb-utils.svg)](https://badge.fury.io/py/indieweb-utils)
[![image](https://img.shields.io/pypi/dm/indieweb-utils)](https://pypistats.org/packages/indieweb-utils)
[![image](https://img.shields.io/pypi/l/indieweb-utils)](https://github.com/capjamesg/indieweb-utils/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/indieweb-utils)](https://badge.fury.io/py/indieweb-utils)

**indieweb-utils** provides building blocks for people implementing IndieWeb applications in Python. Discover IndieWeb endpoints, find feeds on a page, infer page names, generate reply contexts, and more!

The documentation for this project is available at [indieweb-utils.readthedocs.io](https://indieweb-utils.readthedocs.io/en/latest/).

## Installation 💻

To get started, pip install `indieweb-utils`:

    pip install indieweb-utils

## Quickstart ⚡

Here are a few quick code snippets for actions enabled by IndieWeb Utils.

### get reply context about a URL

``` python
import indieweb_utils

context = indieweb_utils.get_reply_context(
    url="https://jamesg.blog",
    summary_word_limit=50
)

print(context.name) # "Home | James' Coffee Blog"
```

### Remove tracking parameters from a URL

``` python
import indieweb_utils

url = "https://jamesg.blog/indieweb/?utm_source=twitter&utm_medium=social&utm_campaign=webmention"

url_without_tracking = indieweb_utils.remove_tracking_params(url)

print(url_without_tracking) # https://jamesg.blog/indieweb/
```

### Create a paginator for a series

``` python
import indieweb_utils

pages = indieweb_utils.Paginator(["post1", "post2", ...], 1)

print(pages.next_page()) [["post1"]]
```

## License 👩‍⚖️

The code in this project is licensed under the [Zero-Clause BSD
License](LICENSE.md).

The documentation in this project is licensed under a [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).

## Running Tests 🧪

Quality is maintained ensuring each merged passes testing, typing, linting, and formatting requirements.

To check locally install the development dependencies and run the suite using [tox]{.title-ref}.

    $ pip install -r requirements_dev.txt
    $ tox

Alternatively, you can run just a single check by passing the environment to tox.

### Unit Tests

Tests use pytest.

    $ tox -e py39  # Run all tests
    $ tox -e py39 tests/test_indieweb_utils.py::TestPostTypeDiscovery  # Run a single test

### Linting

Linting is checked with black, isort, and flake8.

    $ tox -e lint

Black and isort errors can be fixed automatically. Use fmt to fix those errors automatically.

    $ tox -e fmt

### Typing

Types are validated with mypy.

    $ tox -e typecheck

## Contributing 🛠️

This project welcomes contributions from anyone who wants to improve the
library.

Please see the [contributing guidelines](CONTRIBUTING.md) for more
information on how to contribute to the repository.

## Contributors 💻

-   [capjamesg](https://github.com/capjamesg)
-   [tantek](https://github.com/tantek)
-   [jamesvandyne](https://github.com/jamesvandyne)
-   [angelogladding](https://github.com/angelogladding)

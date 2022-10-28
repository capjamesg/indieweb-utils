Python indieweb-utils Library
=======================================

.. image:: https://readthedocs.org/projects/indieweb-utils/badge/?version=latest
   :target: https://indieweb-utils.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**indieweb-utils** is a Python library that provides building blocks for people implementing IndieWeb applications. This library contains implementations for some specifications that may be useful in IndieWeb applications.

This project is under active development.

The documentation for this project is available at `indieweb-utils.readthedocs.io <https://indieweb-utils.readthedocs.io/en/latest/>`_.

License
-------

The code in this project is licensed under the `Zero-Clause BSD License <LICENSE.md>`_.

The documentation in this project is licensed under a `CC BY-SA 4.0 license <https://creativecommons.org/licenses/by-sa/4.0/>`_.

Dependencies
--------------

This project uses the following dependencies:

- BeautifulSoup4 for HTML parsing
- mf2py for microformats parsing
- requests for making HTTP requests


Running Tests
---------------

Quality is maintained ensuring each merged passes testing, typing, linting, and formatting requirements.

To check locally install the development dependencies and run the suite using `tox`.

::

  $ pip install -r requirements_dev.txt
  $ tox

Alternatively, you can run just a single check by passing the environment to tox.

Unit Tests
~~~~~~~~~~~~~~

Tests use pytest.

::

  $ tox -e py39  # Run all tests
  $ tox -e py39 tests/test_indieweb_utils.py::TestPostTypeDiscovery  # Run a single test

Linting
~~~~~~~~~~~~

Linting is checked with black, isort, and flake8.

::

  $ tox -e lint

Black and isort errors can be fixed automatically. Use the `fmt` to fix those errors automatically.

::

  $ tox -e fmt

Typing
~~~~~~~~~~~~

Types are validated with mypy.

::

  $ tox -e typecheck


Contributing
---------------

This project welcomes contributions from anyone who wants to improve the library.

Please see the `contributing guidelines <CONTRIBUTING.md>`_ for more information on how to contribute to the repository.

Contributors
------------

- `capjamesg <https://github.com/capjamesg>`_
- `tantek <https://github.com/tantek>`_
- `jamesvandyne <https://github.com/jamesvandyne>`_
- `angelogladding <https://github.com/angelogladding>`_

Usage
=====

.. _installation:

.. toctree::

Installation
------------------------

To install this package, run the following command:

.. code-block:: python

    pip install indieweb-utils

You can import the package using the following line of code:

.. code-block:: python

    import indieweb_utils

Infer the Name of a Page
------------------------

To find the name of a page per the `Page Name Discovery Algorithm <https://indieweb.org/page-name-discovery>`_, use this function:

.. autofunction:: indieweb_utils.get_page_name

This function searches:

1. For a h-entry title;
2. For a h-entry summary;
3. For a HTML page <title> tag;
4. Otherwise, returns "Untitled".
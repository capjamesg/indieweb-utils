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

Canonicalize a URL
------------------------

Canonicalization turns a relative URL into a complete URL.

To canonicalize a URL, use this function:

.. autofunction:: indieweb_utils.canonicalize_url

This function returns a URL with a protocol, host, and path.

The domain of the resource is needed so that it can be added to the URL during canonicalization if the URL is relative.

A complete URL returned by this function looks like this:

.. code-block:: python

    https://indieweb.org/POSSE


Generate Reply Context
------------------------

To generate reply context for a given page, use the following function:

.. autofunction:: indieweb_utils.get_reply_context

This function returns a ReplyContext object that looks like this:

.. autoclass:: indieweb_utils.ReplyContext

Generate a URL Summary
----------------------

You can generate a summary of a URL without retrieving the page using the `get_url_summary` function.

By default, this function can generate a summary for the following URLs:

- github.com
- twitter.com
- eventbrite.com / eventbrite.co.uk
- upcoming.com
- calagator.com
- events.indieweb.org
- indieweb.org

.. autofunction:: indieweb_utils.get_url_summary

You can specify custom mappings for other domains using the `custom_mappings` parameter.

This parameter accepts a dictionary of with domain names mapped to lists of tuples with patterns to match and strings to return, like this:

    {
        "example.com": [
            (r"example.com/(\d+)", "Example #{}"),
        ]
    }

If a summary cannot be generated, this function returns "A post by [domain_name].", where domain name is the domain of the URL you passed into the function.


Get a Page h-feed
---------------------------

The `discover_page_feed()` function implements the proposed `microformats2 h-feed discovery algorithm <https://microformats.org/wiki/h-feed#Discovery>`_.

This function looks for a h-feed on a given page. If one is not found, the function looks for a rel tag to a h-feed. If one is found, that document is parsed.

If a h-feed is found on the related document, the h-feed is returned.

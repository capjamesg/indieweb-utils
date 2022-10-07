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


Custom Properties
------------------------

The structure of the custom properties tuple is:

.. code-block:: python

   (attribute_to_look_for, value_to_return)

An example custom property value is:

.. code-block:: python

    custom_properties = [
        ("poke-of", "poke")
    ]

This function would look for a poke-of attribute on a web page and return the "poke" value.

By default, this function contains all of the attributes in the Post Type Discovery mechanism.

Custom properties are added to the end of the post type discovery list, just before the "article" property. All specification property types are checked before your custom attribute.

Discover an Endpoint
-----------------------------

You can discover an endpoint from a HTTP header or a HTML `link` tag using the `discover_endpoint` function.

The `discover_endpoint` function uses this syntax:

.. autofunction:: indieweb_utils.discover_endpoint

Here are some example values for use with this function:

.. codeblock:: python

    headers_to_find = ["indieauth-metadata"] # discover an IndieAuth metadata endpoint
    headers_to_find = ["authorization_endpoint", "token_endpoint"] # discover IndieAuth authorization and token endpoints
    headers_to_find = ["hub", "self"] # discover WebSub endpoints
    headers_to_find = ["micropub"] # discover a Micropub endpoint
    headers_to_find = ["microsub"] # discover a Microsub endpoint
    headers_to_find = ["syndication", "shortlink"] # useful for interpreting Micropub success responses (ref: https://www.w3.org/TR/micropub/#h-response)

Discover a Webmention Endpoint
------------------------------------

Webmention endpoint discovery is useful if you want to know if you can send webmentions to a site or if you want to send a webmention to a site.

This function both finds a Webmention endpoint and validates it. This function should be used to discover Webmention endpoints instead of `discover_endpoint()`, which is more generic and performs no validation on resources it discovers.

You can discover if a URL has an associated webmention endpoint using the `discover_webmention_endpoint` function:

.. autofunction:: indieweb_utils.discover_webmention_endpoint

If successful, this function returns the URL of the webmention endpoint associated with a resource. In this case, the message value is a blank string.

If a webmention endpoint could not be found, URL is equal to None. In this case, a string message value is provided that you can use for debugging or present to a user.

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


Get a Page h-feed
---------------------------

The `discover_page_feed()` function implements the proposed `microformats2 h-feed discovery algorithm <https://microformats.org/wiki/h-feed#Discovery>`_.

This function looks for a h-feed on a given page. If one is not found, the function looks for a rel tag to a h-feed. If one is found, that document is parsed.

If a h-feed is found on the related document, the h-feed is returned. 


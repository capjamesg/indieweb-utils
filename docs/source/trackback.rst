Trackbacks
==========

This library includes support for Trackback URL Discovery and sending Trackbacks.

Trackback URL discovery
-----------------------

The IndieWeb Utils Trackback discovery performs the following steps:

1. Checks for a `trackback:ping` attribute in an RDF comment. If one is found, this is returned.
2. Checks for an `EditURI` `<link>` tag. If one is found, its contents are retrieved. If the contents contain a `trackback:ping` attribute, this is returned.

.. code-block:: python

    from indieweb_utils import discover_trackback_url

    discover_trackback_url('http://example.com/post/123')


Send a Trackback
----------------

The `send_trackback` function sends a Trackback to a given URL. Discovery is performed on the `target_url` to find its Trackback endpoint, to which a Trackback is sent.

.. code-block:: python

    from indieweb_utils import send_trackback

    send_trackback(
        target_url='http://example.com/post/123',
        source_url='http://example.com/post/123#trackback',
        title='My Post',
        excerpt='This is my post',
        blog_name='My Blog'
    )

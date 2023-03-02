Trackbacks
==========

This library includes support for `Trackback <http://archive.cweiske.de/trackback/trackback-1.2.html>`_ URL Discovery and sending Trackbacks.

Trackback URL discovery
-----------------------

The IndieWeb Utils Trackback discovery performs the following steps:

1. Checks for a `trackback:ping` attribute in an RDF comment. If one is found, this is returned.
2. Checks for an `EditURI` `<link>` tag. If one is found, its contents are retrieved. If the contents contain a `trackback:ping` attribute, this is returned.

.. autofunction:: indieweb_utils.discover_trackback_url

Send a Trackback
----------------

The `send_trackback` function sends a Trackback to a given URL. Discovery is performed on the `target_url` to find its Trackback endpoint, to which a Trackback is sent.

.. autofunction:: indieweb_utils.send_trackback

Validate a Trackback
--------------------

The `process_trackback` function validates data from a trackback response sent to an endpoint. You can use this function to:

1. Make sure a request has the required content type and method. If an error is found, a string with an RDF error is returned that can be sent by the server back to the client;
2. Send an error response if the source site is not in a list of allowed sites (optional) and;
3. Send a success response if the Trackback is valid.

.. autofunction:: indieweb_utils.process_trackback
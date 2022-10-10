Webmention
===========


Discover a Webmention Endpoint
------------------------------------

Webmention endpoint discovery is useful if you want to know if you can send webmentions to a site or if you want to send a webmention to a site.

You can discover if a URL has an associated webmention endpoint using the `discover_webmention_endpoint` function:

.. autofunction:: indieweb_utils.discover_webmention_endpoint

If successful, this function returns the URL of the webmention endpoint associated with a resource. In this case, the message value is a blank string.

If a webmention endpoint could not be found, URL is equal to None. In this case, a string message value is provided that you can use for debugging or present to a user.


Send a Webmention
------------------

To send a webmention to a target, use this function:

.. autofunction:: indieweb_utils.send_webmention

This function returns a SendWebmentionResponse object with this structure:

.. autoclass:: indieweb_utils.SendWebmentionResponse
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


Handle an IndieAuth Callback Request
------------------------------------

The last stage of the IndieAuth authentication flow for a client is to verify a callback response and exchange the provided code with a token.

This function implements a callback handler to verify the response frmo an authorization server and redeem a token.

To use this function, you need to pass in the following arguments:

.. autofunction:: indieweb_utils.indieauth_callback_handler

This function verifies that an authorization server has returned a valid response and redeems a token.

You can leave the "me" value equal to None if any URL should be able to access your service.

Otherwise, set "me" to the URL of the profile that should be able to access your service.

Setting a me value other than None may be useful if you are building personal services that nobody else should be able to access.

If successful, this function returns an IndieAuthCallbackResponse object that looks like this:

.. class:: indieweb_utils.IndieAuthCallbackResponse

This class contains an endpoint_response value. This value is equal to the JSON response sent by the IndieAuth web server.

An example endpoint response looks like this:

.. code-block:: python

    {
        "me": "https://jamesg.blog/",
        "access_token": "ACCESS_TOKEN",
        "scope": "SCOPE_LIST"
    }

Check if a User is Authenticated (Flask)
----------------------------------------

To check if a user is authenticated in a Flask application, use the following function:

.. autofunction:: indieweb_utils.is_authenticated

This function checks if an authorization token is provided in a header or user storage. If a token is provided, that token is verified with the specified token endpoint.

A True value is returned if a user has provided a token and that token is valid. A False value is returned if a user has not provided a token or if the token is invalid.

Generate Reply Context
------------------------

To generate reply context for a given page, use the following function:

.. autofunction:: indieweb_utils.get_reply_context

This function returns a ReplyContext object that looks like this:

.. autoclass:: indieweb_utils.ReplyContext


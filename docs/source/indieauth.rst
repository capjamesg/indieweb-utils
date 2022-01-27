IndieWeb Utils IndieAuth Features
=================================

The indieweb-utils library provides a number of helper functions that will enable you
to implement your own IndieAuth authentication and token endpoints in Python.

These functions may be useful if you want to bundle an authentication and token provider
with a service you are building, such as a personal blog or a social reader.

This page outlines how to use the IndieAuth features provided in this library.

Get application scope reference
-------------------------------

The library comes with a constant variable that lists various scopes that are commonly
used in IndieWeb community applications. These scopes cover values you might see in 
Micropub, Microsub, and other applications.

You may want to use this reference to give a user additional information about the scopes 
to which they are granting access by authenticating with a service.

To access the scope reference, import the following variable:

..code-block:: python

    from indieweb_utils import SCOPE_DEFINITIONS

Get a h-app object
------------------

You might want to retrieve a h-app object to show context to the user about the application
that is requesting a user to authenticate.

You can do this using the following function:

    ..autofunction:: indieweb_utils.get_h_app_item

This function returns an object with the name, logo, url, and summary found in a h-app item.

Note: The h-app item is not widely supported. As a result, you might want to add a fallback in the case
that the h-app function does not find any values to return.

Get a profile response object
-----------------------------

If you want your IndieAuth object to return profile information when the "profile" scope 
is requested, the get_profile() function may come in handy.

This function takes a URL and retrieves the name, photo, url, and email properties found on the h-card 
of the specified page. If a h-card is not provided, empty strings are returned.

Usage information for this function is below.

    ..autofunction:: indieweb_utils.get_profile

Generate an authentication token
--------------------------------

Validate an authorization response
----------------------------------

Verify a decoded code
---------------------

Redeem an IndieAuth code
------------------------

Validate an access token
------------------------
IndieAuth
==========

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

.. code-block:: python

    from indieweb_utils import SCOPE_DEFINITIONS

Get a h-app object
------------------

You might want to retrieve a h-app object to show context to the user about the application
that is requesting a user to authenticate.

You can do this using the following function:

.. autofunction:: indieweb_utils.get_h_app_item

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

.. autofunction:: indieweb_utils.get_profile



Retrieve Valid Links for Use in RelMeAuth
-----------------------------------------

To authenticate a user with `RelMeAuth <https://microformats.org/RelMeAuth>`_, you need to validate that there is a two-way link between two resources.

IndieWeb Utils implements a helper function that checks whether the URLs linked with rel=me on a web page contain a
link back to the source.

To check whether there is a two-way rel=me link between two resources, you can use this function:

.. autofunction:: indieweb_utils.get_valid_relmeauth_links

This function does not check whether a URL has an OAuth provider. Your application should check the list of valid
rel me links and only use those that integrate with the OAuth providers your RelMeAuth service supports. For example,
if your service does not support Twitter, you should not present Twitter as a valid authentication option to a user, even if the `get_valid_relmeauth_links()` function found a valid two-way rel=me link.


IndieAuth Endpoint Scaffolding
--------------------------------

indieweb-utils includes a `indieauth.server` module with scaffolding to help you build your own IndieAuth endpoints.


Generate an authentication token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `generate_auth_token()` function validates that an authentication request contains all required values. Then,
this function generates a JWT-encoded token with the following pieces of information:

- me
- code_verifier
- expires
- client_id
- redirect_uri
- scope
- code_challenge
- code_challenge_method

You can later refer to these values during the stage where you decode a token.

Here is the syntax for this function:

.. autofunction:: indieweb_utils.indieauth.server.generate_auth_token

This function returns both the code you should send to the client in the authentication redirect
response as well as the code_verifier used in the token. This code_verifier should be saved,
perhaps in session storage, for later use in checking the validity of a token redemption
request.

Validate an authorization response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `_validate_indieauth_response` function contains five checks. These five checks validate an authorization response according to the IndieAuth specification.

1. Ensures the grant_type provided is authorization_code.
2. Validates that a code, client_id, and redirect_uri are provided.
3. Checks that the code challenge method provided is allowed.
4. Verifies the length of the code challenge is within the range of 43 and 128 characters.

You should use this function to ensure a POST request to an authorization endpoint to
redeem an authorization code (per `5.3 Redeeming the Authorization Code <https://indieauth.spec.indieweb.org/#redeeming-the-authorization-code>`_ in the IndieAuth spec)
is valid.

Here is the syntax for this function:

.. autofunction:: indieweb_utils.validate_authorization_response

This function does not return a value if an authorization response is valid. If a response is invalid,
an exception will be raised with a relevant error message.

Redeem an IndieAuth code at a token endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can redeem an IndieAuth authorization code for an access token if needed. This is a common
need for Micropub and Microsub clients.

The `redeem_code()` function validates all the required parameters are provided in a request. Then,
this function decodes the provided code using the code, secret key, and algorithm specified. If
the code is invalid or the code challenge in the decoded code is invalid, AuthenticationErrors will be
raised. The function will also verify that:

1. An authorization code has not expired.
2. The specified redirect URI matches the decoded redirect URI.
3. The specified client ID matches the decoded client ID.

Finally, this function encodes an access token that you can return in response to a request to create
a token for a token endpoint.

Here is the syntax for this function:

.. autofunction:: indieweb_utils.redeem_code


Validate an access token created by a token endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A server may ask your token endpoint to validate that a provided token is in fact valid. This may be done
by a Micropub client to ensure a token is still active, for example.

You can validate an access token using the `validate_access_token()` function.

This function decodes an authorization code using the specified secret key and algorithm(s). Then, the function
will check that the authorization code has not yet expired.

If the code can be decoded, the me, client_id, and scope values will be returned.

Here is the syntax for the function:

.. autofunction:: indieweb_utils.validate_access_token

Determine if a user is authenticated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if a user is authenticated in a Flask application, use the following function:

.. autofunction:: indieweb_utils.is_authenticated

This function checks if an authorization token is provided in a header or user storage. If a token is provided, that token is verified with the specified token endpoint.

A True value is returned if a user has provided a token and that token is valid. A False value is returned if a user has not provided a token or if the token is invalid.


Handle an IndieAuth callback request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The last stage of the IndieAuth authentication flow for a client is to verify a callback response and exchange the provided code with a token.

This function implements a callback handler to verify the response frmo an authorization server and redeem a token.

To use this function, you need to pass in the following arguments:

.. autofunction:: indieweb_utils.indieauth_callback_handler

This function verifies that an authorization server has returned a valid response and redeems a token.

You can leave the "me" value equal to None if any URL should be able to access your service.

Otherwise, set "me" to the URL of the profile that should be able to access your service.

Setting a me value other than None may be useful if you are building personal services that nobody else should be able to access.

If successful, this function returns an IndieAuthCallbackResponse object that contains:

.. autofunction:: indieweb_utils.IndieAuthCallbackResponse

This class contains a `response` value. This value is equal to the JSON response sent by the IndieAuth web server.

An example endpoint response looks like this:

.. code-block:: python

    {
        "me": "https://jamesg.blog/",
        "access_token": "ACCESS_TOKEN",
        "scope": "SCOPE_LIST"
    }

This function does not check whether a URL has an OAuth provider. Your application should check the list of valid
rel me links and only use those that integrate with the OAuth providers your RelMeAuth service supports. For example,
if your service does not support Twitter, you should not present Twitter as a valid authentication option to a user, even if the `get_valid_relmeauth_links()` function found a valid two-way rel=me link.

IndieAuth Login Scaffolding (Flask)
-----------------------------------

The `indieweb_utils.indieauth.decorators` module contains functions useful for building authentication systems with Flask.

These functions are Flask-specific.

Initiate an authentication request
----------------------------------

The `discover_auth_endpoint_decorator` function is meant to be used as a response to an endpoint on your site that discovers the IndieAuth endpoint for a given URL.

This function discovers the IndieAuth endpoint for a resource then redirects a user to their IndieAuth endpoint to verify their identity.

.. autofunction:: indieweb_utils.discover_auth_endpoint_decorator

Handle an IndieAuth callback request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `indieauth_callback_response()` function should be used as a response to a callback endpoint on your site. This endpoint should be equal to the `callback_url` specified in the `discover_auth_endpoint_decorator` function.

.. autofunction:: indieweb_utils.indieauth_callback_response

This function will:

1. Call the low-level `indieauth_callback_handler` function to verify the callback response.
2. Set three values in your Flask session: `me`, `access_token`, and `scope`.
3. Redirect you to the `redirect_success_destination` argument provided in the function.

If there is an error, a user will be redirected to the value of the `redirect_error_destination` argument.
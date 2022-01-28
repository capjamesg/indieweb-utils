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

The generate_auth_token() validates that an authentication request contains all required values. Then,
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

This function returns both the code you should send to the client in the authentication redirect
response as well as the code_verifier used in the token. This code_verifier should be saved,
perhaps in session storage, for later use in checking the validity of a token redemption
request.

Validate an authorization response
----------------------------------

The validate_authorization_response() function contains five checks:

1. Ensures the grant_type provided is authorization_code.
2. Validates that a code, client_id, and redirect_uri are provided.
3. Checks that the code challenge method provided is allowed.
4. Verifies the length of the code challenge is within the range of 43 and 128 characters.

You should use this function to ensure a POST request to an authorization endpoint to
redeem an authorization code (per 5.3 Redeeming the Authorization Code in the IndieAuth spec)
is valid.

Here is the syntax for this function:

    ..autofunction:: indieweb_utils.validate_authorization_response

Redeem an IndieAuth code at a token endpoint
--------------------------------------------

You can redeem an IndieAuth authorization code for an access token if needed. This is a common
need for Micropub and Microsub clients.

The redeem_code() function validates all the required parameters are provided in a request. Then,
this function decodes the provided code using the code, secret key, and algorithm specified. If
the code is invalid or the code challenge in the decoded code is invalid, AuthenticationErrors will be
raised. The function will also verify that:

1. An authorization code has not expired.
2. The specified redirect URI matches the decoded redirect URI.
3. The specified client ID matches the decoded client ID.

Finally, this function encodes an access token that you can return in response to a request to create
a token for a token endpoint.

Here is the syntax for this function:

    ..autofunction:: indieweb_utils.redeem_code

Validate an access token created by a token endpoint
----------------------------------------------------

A server may ask your token endpoint to validate that a provided token is in fact valid. This may be done
by a Micropub client to ensure a token is still active, for example.

You can validate an access token using the validate_access_token() function.

This function decodes an authorization code using the specified secret key and algorithm(s). Then, the function
will check that the authorization code has not yet expired.

If the code can be decoded, the me, client_id, and scope values will be returned.

Here is the syntax for the function:

    ..autofunction:: indieweb_utils.validate_access_token
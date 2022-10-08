import base64
import binascii
import hashlib
import os
import time
from dataclasses import dataclass

import jwt


def generate_token(*, size: int = 20) -> str:
    return binascii.hexlify(os.urandom(size)).decode()


class AuthenticationError(Exception):
    pass


class TokenValidationError(Exception):
    pass


class AuthorizationCodeExpiredError(Exception):
    pass


@dataclass
class DecodedAuthToken:
    me: str
    client_id: str
    scope: str
    decoded_authorization_code: dict


@dataclass
class AuthTokenResponse:
    code: str
    code_verifier: str
    code_challenge: str


@dataclass
class TokenEndpointResponse:
    access_token: str
    token_type: str
    scope: str
    me: str


def validate_authorization_response(
    grant_type: str,
    code: str,
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
    code_challenge_method: str,
    allowed_methods: list = ["S256"],
) -> None:
    """
    Conducts checks to validate the response from an IndieAuth authorization endpoint.

    :param grant_type: The grant type of the authorization request.
    :type grant_type: str
    :param code: The code returned from the authorization request.
    :type code: str
    :param client_id: The client ID of the authorization request.
    :type client_id: str
    :param redirect_uri: The redirect URI of the authorization request.
    :type redirect_uri: str
    :param code_challenge: The code challenge, used for PKCE.
    :type code_challenge: str
    :param code_challenge_method: The code challenge method, used for PKCE.
    :type code_challenge_method: str
    :param allowed_methods: The list of allowed code challenge methods (default: ["S256"]).
    :type allowed_methods: list
    :returns: A boolean indicating whether the response is valid.
    :rtype: bool

    Example:

    .. code-block:: python

        import indieweb_utils

        indieweb_utils.validate_authorization_response(
            grant_type="authorization_code",
            code="12345",
            client_id="https://example.com",
            redirect_uri="https://example.com/callback",
            code_challenge="12345",
            code_challenge_method="S256",
            allowed_methods=["S256"]
        )

    :raises TokenValidationError: If the response is invalid.
    """

    if grant_type != "authorization_code":
        raise TokenValidationError("Only authorization_code grant types are supported.")

    if not all([code, client_id, redirect_uri]):
        raise TokenValidationError("Token request is missing required parameters.")

    if code_challenge and code_challenge_method:
        if code_challenge_method not in allowed_methods:
            raise TokenValidationError("The challenge method provided is not supported.")

        if len(code_challenge) < 43:
            raise TokenValidationError("The challenge provided is too short.")

        if len(code_challenge) > 128:
            raise TokenValidationError("The challenge provided is too long.")


def _verify_decoded_code(
    client_id: str, redirect_uri: str, decoded_client_id: str, decoded_redirect_uri: str, decoded_expires: int
) -> bool:
    """
    Conducts checks to validate the decoded code in an authorization request.

    :param client_id: The client ID of the authorization request.
    :rtype: str
    :param redirect_uri: The redirect URI of the authorization request.
    :rtype: str
    :param decoded_client_id: The decoded client ID of the authorization request.
    :rtype: str
    :param decoded_redirect_uri: The decoded redirect URI of the authorization request.
    :rtype: str
    :param decoded_expires: The decoded expiration time of the authorization request.
    :rtype: int
    :returns: True if the decoded code is valid, False otherwise.
    :rtype: bool

    Example:

    .. code-block:: python

        import indieweb_utils

        client_id = "https://example.com"
        redirect_uri = "https://example.com/callback"
        decoded_client_id = "https://example.com"
        decoded_redirect_uri = "https://example.com/callback"
        decoded_expires = 3600

            code_is_valid = indieweb_utils.indieauth.server._verify_decoded_code(
            client_id,
            redirect_uri,
            decoded_client_id,
            decoded_redirect_uri,
            decoded_expires
        )

    :raises AuthorizationCodeExpiredError: If the authorization code has expired.
    :raises TokenValidationError: If the decoded code is invalid.
    """

    if int(time.time()) > decoded_expires:
        raise AuthorizationCodeExpiredError("The authorization code has expired.")

    if redirect_uri != decoded_redirect_uri:
        raise TokenValidationError(
            "The redirect URI provided does not match the redirect URI in the authorization token."
        )

    if client_id != decoded_client_id:
        raise TokenValidationError("The client ID provided does not match the client ID in the authorization token.")

    return True


def generate_auth_token(
    me: str,
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str,
    code_challenge_method: str,
    final_scope: str,
    secret_key: str,
    **kwargs
) -> AuthTokenResponse:
    """
    Generates an IndieAuth authorization token.

    :param me: The URL of the user's profile.
    :type me: str
    :param client_id: The client ID of the authorization request.
    :type client_id: str
    :param redirect_uri: The redirect URI of the authorization request.
    :type redirect_uri: str
    :param response_type: The response type of the authorization request.
    :type response_type: str
    :param state: The state of the authorization request.
    :type state: str
    :param code_challenge_method: The code challenge method, used for PKCE.
    :type code_challenge_method: str
    :param final_scope: The scopes approved by the user.
    :type final_scope: str
    :param secret_key: The secret key used to sign the token.
    :type secret_key: str
    :param kwargs: Additional parameters to include in the token.
    :type kwargs: dict
    :returns: The authorization token.
    :rtype: str

    Example:

    .. code-block:: python

        import indieweb_utils
        import random
        import string
        token = indieweb_utils.indieauth.server.generate_auth_token(
            me="https://test.example.com/user",
            client_id="https://example.com",
            redirect_uri="https://example.com/callback",
            response_type="code",
            state="".join(random.choice(string.ascii_letters) for _ in range(32)),
            code_challenge_method="S256",
            final_scope="read write",
            secret_key="secret"
        )

    :raises AuthenticationError: Authentication request is invalid.
    """

    if not all([client_id, redirect_uri, response_type, state]):
        raise AuthenticationError("Token request is missing required parameters.")

    if response_type not in ["code", "id"]:
        raise AuthenticationError("Only code and id response types are supported.")

    code_verifier = generate_token()

    sha256_code = hashlib.sha256(code_verifier.encode("utf-8")).hexdigest()

    code_challenge = base64.urlsafe_b64encode(sha256_code.encode("utf-8")).decode("utf-8")

    encoded_code = jwt.encode(
        {
            "me": me,
            "code_verifier": code_verifier,
            "expires": int(time.time()) + 3600,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": final_scope,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
            **kwargs,
        },
        secret_key,
        algorithm="HS256",
    )

    return AuthTokenResponse(code=encoded_code, code_verifier=code_verifier, code_challenge=code_challenge)


def redeem_code(
    grant_type: str,
    code: str,
    client_id: str,
    redirect_uri: str,
    code_verifier: str,
    secret_key: str,
    algorithms: list = ["HS256"],
    **kwargs
) -> TokenEndpointResponse:

    """
    Redeems an IndieAuth code for an access token.

    :param grant_type: The grant type of the authorization request.
    :type grant_type: str
    :param code: The code returned from the authorization request.
    :type code: str
    :param client_id: The client ID of the authorization request.
    :type client_id: str
    :param redirect_uri: The redirect URI of the authorization request.
    :type redirect_uri: str
    :param code_verifier: The code verifier, used for PKCE.
    :type code_verifier: str
    :param secret_key: The secret key used to sign the token.
    :type secret_key: str
    :param algorithms: The list of algorithms to use for signing the token (default: ["HS256"]).
    :type algorithms: list
    :param kwargs: Additional parameters to include in the token.
    :type kwargs: dict
    :returns: A token endpoint response object.
    :rtype: TokenEndpointResponse

    Example:

    .. code-block:: python

        import indieweb_utils

        token_response = indieweb_utils.indieauth.server.redeem_code(
            grant_type="authorization_code",
            code="code",
            client_id="https://example.com",
            redirect_uri="https://example.com/callback",
            code_verifier="code_verifier",
            secret_key="secret"
        )

        print(token_response.access_token)
        print(token_response.token_type)
        print(token_response.scope)
        print(token_response.me)

    :raises AuthorizationCodeExpiredError: If the authorization code has expired.
    :raises TokenValidationError: If the decoded code is invalid.
    :raises AuthenticationError: If the token request is invalid.
    """

    if not code or not client_id or not redirect_uri or not grant_type:
        raise AuthenticationError("A code, client_id, redirect_uri, and grant_type must be provided.")

    if grant_type != "authorization_code":
        raise AuthenticationError("Only authorization_code grant types are accepted.")

    try:
        decoded_code = jwt.decode(code, secret_key, algorithms=algorithms)
    except jwt.InvalidTokenError:
        raise AuthenticationError("Code is invalid.")

    if code_verifier is not None and decoded_code["code_challenge_method"] == "S256":
        sha256_code = hashlib.sha256(code_verifier.encode("utf-8")).hexdigest()

        # urls must be encoded with url safe base64, not just standard base64
        code_challenge = base64.urlsafe_b64encode(sha256_code.encode("utf-8")).decode("utf-8")

        if code_challenge != decoded_code["code_challenge"]:
            raise AuthenticationError("Code challenge in decoded code was invalid.")

    valid = _verify_decoded_code(
        client_id, redirect_uri, decoded_code["client_id"], decoded_code["redirect_uri"], decoded_code["expires"]
    )

    if not valid:
        raise AuthenticationError(valid)

    scope = decoded_code["scope"]
    me = decoded_code["me"]

    access_token = jwt.encode(
        {
            "me": me,
            "expires": int(time.time()) + 360000,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            **kwargs,
        },
        secret_key,
        algorithm="HS256",
    )

    return TokenEndpointResponse(access_token=access_token, token_type="bearer", scope=scope, me=me)


def validate_access_token(
    authorization_code: str,
    secret_key: str,
    algorithms: list = ["HS256"],
) -> DecodedAuthToken:
    """
    Validates an access token provided by a token endpoint.

    :param authorization_code: The authorization code returned from the authorization request.
    :type authorization_code: str
    :param secret_key: The secret key used to sign the token.
    :type secret_key: str
    :param algorithms: The algorithms used to sign the token (default: ["HS256"]).
    :type algorithms: list
    :returns: An object with the me, client_id, and scope values from the access token.
    :rtype: DecodedAuthToken

    Example:

    .. code-block:: python

        import indieweb_utils

        try:
            decoded_token = indieweb_utils.indieauth.server.validate_access_token(
                authorization_code="code",
                secret_key="secret"
            )

            print(decoded_token.me)
            print(decoded_token.client_id)
            print(decoded_token.scope)
            print(decoded_token.decoded_authorization_code)
        except indieweb_utils.AuthenticationError as e:
            print(e)
        except indieweb_utils.AuthorizationCodeExpiredError as e:
            print(e)

    :raises AuthorizationCodeExpiredError: Authorization code has expired.
    :raises AuthenticationError: Authorization code provided is invalid.
    """

    try:
        decoded_authorization_code = jwt.decode(authorization_code, secret_key, algorithms=algorithms)
    except jwt.InvalidTokenError:
        raise AuthenticationError("Authorization code is invalid.")

    if int(time.time()) > decoded_authorization_code["expires"]:
        raise AuthorizationCodeExpiredError("Authorization code has expired.")

    me = decoded_authorization_code["me"]
    client_id = decoded_authorization_code["client_id"]
    scope = decoded_authorization_code["scope"]

    return DecodedAuthToken(
        me=me, client_id=client_id, scope=scope, decoded_authorization_code=decoded_authorization_code
    )

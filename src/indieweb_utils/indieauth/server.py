import time
import random
import string
import jwt

class AuthenticationError(Exception):
    pass

def validate_authorization_response(
        grant_type: str,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        code_challenge_method: str,
        allowed_methods: list = ["S256"]
    ) -> bool:
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

        :returns: True if the response is valid, False otherwise.
        :rtype: bool
    """

    if grant_type != "authorization_code":
        return False

    if not code or not client_id or not redirect_uri:
        return False

    if code_challenge and code_challenge_method:
        if code_challenge_method not in allowed_methods:
            return False

        if len(code_challenge) < 43:
            return False

        if len(code_challenge) > 128:
            return False

    return True

def verify_decoded_code(
        client_id: str,
        redirect_uri: str,
        decoded_client_id: str,
        decoded_redirect_uri: str,
        decoded_expires: int
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
    """

    if int(time.time()) > decoded_expires:
        return False

    if redirect_uri != decoded_redirect_uri:
        return False

    if client_id != decoded_client_id:
        return False

    return True

def generate_auth_token(
        me: str,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        state: str,
        code_challenge: str,
        code_challenge_method: str,
        final_scope: str,
        secret_key: str
    ) -> str:
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
        :param code_challenge: The code challenge, used for PKCE.
        :type code_challenge: str
        :param code_challenge_method: The code challenge method, used for PKCE.
        :type code_challenge_method: str
        :param final_scope: The scopes approved by the user.
        :type final_scope: str
        :param secret_key: The secret key used to sign the token.
        :type secret_key: str
        :returns: The authorization token.
        :rtype: str
    """

    if not client_id or not redirect_uri or not response_type or (not state and state != ""):
        raise AuthenticationError("Token request is missing required parameters.")

    if response_type != "code" and response_type != "id":
        raise AuthenticationError("Only code and id response types are supported.")

    random_string = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    encoded_code = jwt.encode(
        {
            "me": me,
            "random_string": random_string,
            "expires": int(time.time()) + 3600,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": final_scope,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method
        },
        secret_key,
        algorithm="HS256"
    )

    return encoded_code

def generate_indieauth_token(

)
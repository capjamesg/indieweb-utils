from dataclasses import dataclass
from typing import List

import requests


@dataclass
class IndieAuthCallbackResponse:
    message: str
    response: dict


class AuthenticationError(Exception):
    pass


def _validate_indieauth_response(me: str, response: requests.Response, required_scopes: List[str]) -> None:
    if me is None:
        message = "An invalid me value was provided."
        raise AuthenticationError(message)

    if response.json().get("me").strip("/") != me.strip("/"):
        message = "Your domain is not allowed to access this website."
        raise AuthenticationError(message)

    granted_scopes = response.json().get("scope").split(" ")

    if response.json().get("scope") == "" or any(scope not in granted_scopes for scope in required_scopes):
        message = f"You need to grant {', '.join(required_scopes).strip(', ')} access to use this tool."
        raise AuthenticationError(message)


def indieauth_callback_handler(
    *,
    code: str,
    state: str,
    token_endpoint: str,
    code_verifier: str,
    session_state: str,
    me: str,
    callback_url: str,
    client_id: str,
    required_scopes: List[str],
) -> IndieAuthCallbackResponse:
    """
    Exchange a callback 'code' for an authentication token.

    :param code: The callback 'code' to exchange for an authentication token.
    :type code: str
    :param state: The state provided by the authentication server in the callback response.
    :type state: str
    :param token_endpoint: The token endpoint to use for exchanging the callback 'code' for an authentication token.
    :type token_endpoint: str
    :param code_verifier: The code verifier to use for exchanging the callback 'code' for an authentication token.
    :type code_verifier: str
    :param session_state: The state stored in session used to verify the callback state is valid.
    :type session_state: str
    :param me: The URL of the user's profile.
    :type me: str
    :param callback_url: The callback URL used in the original authentication request.
    :type callback_url: str
    :param client_id: The client ID used in the original authentication request.
    :type client_id: str
    :param required_scopes: The scopes required for the application to work.
        This list should not include optional scopes.
    :type required_scopes: list[str]
    :return: A message indicating the result of the callback (success or failure) and the token endpoint response.
        The endpoint response will be equal to None if the callback failed.
    :rtype: tuple[str, dict]
    """

    if state != session_state:
        message = "The provided state value did not match the session state. Please try again."
        raise AuthenticationError(message)

    data = {
        "code": code,
        "redirect_uri": callback_url,
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }

    headers = {"Accept": "application/json"}

    try:
        auth_request = requests.post(token_endpoint, data=data, headers=headers)
    except requests.exceptions.RequestException:
        message = "Your token endpoint server could not be accessed."
        raise AuthenticationError(message)

    if auth_request.status_code != 200:
        message = "There was an error with your token endpoint server."
        raise AuthenticationError(message)

    # remove code verifier from session because the authentication flow has finished

    _validate_indieauth_response(me, auth_request, required_scopes)

    return IndieAuthCallbackResponse(message="Authentication was successful.", response={})


def is_authenticated(token_endpoint: str, headers: dict, session: dict, approved_user: bool = None) -> bool:
    """
    Check if a user has provided a valid Authorization header or access token in session. Designed for use with Flask.

    :param token_endpoint: The token endpoint of the user's IndieAuth server.
    :param headers: The headers sent by a request.
    :param session: The session object from a Flask application.
    :param approved_user: The optional URL of the that is approved to use the API.
    :return: True if the user is authenticated, False otherwise.
    :rtype: bool
    """
    if headers.get("Authorization") is not None:
        access_token = headers["Authorization"].split(" ")[-1]

    elif session.get("access_token"):
        access_token = session.get("access_token")
    else:
        return False

    try:
        check_token = requests.get(token_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=5)
    except requests.exceptions.Timeout:
        raise AuthenticationError("The specified token endpoint timed out.")
    except requests.exceptions.RequestException:
        raise AuthenticationError("The specified token endpoint could not be accessed.")

    if check_token.status_code != 200 or not check_token.json().get("me"):
        return False

    if approved_user is not None and check_token.status_code != 200 and check_token.json()["me"] != approved_user:
        return False

    return True

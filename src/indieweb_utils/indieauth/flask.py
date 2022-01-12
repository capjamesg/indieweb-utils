import requests


def indieauth_callback_handler(
    code, state, token_endpoint, code_verifier, session_state, me, callback_url, client_id, required_scopes
):
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
    :param required_scopes: The scopes required for the application to work. This list should not include optional scopes.
    :type required_scopes: list[str]
    :return: A message indicating the result of the callback (success or failure) and the token endpoint response. The endpoint response will be equal to None if the callback failed.
    :rtype: tuple[str, dict]
    """

    if state != session_state:
        message = "Your authentication failed. Please try again."
        return message, None

    data = {
        "code": code,
        "redirect_uri": callback_url,
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }

    headers = {"Accept": "application/json"}

    try:
        r = requests.post(token_endpoint, data=data, headers=headers)
    except:
        message = "Your token endpoint server could not be accessed."
        return message, None

    if r.status_code != 200:
        message = "There was an error with your token endpoint server."
        return message, None

    # remove code verifier from session because the authentication flow has finished

    if me is None:
        message = "An invalid me value was provided."

        return message, None

    if r.json().get("me").strip("/") != me.strip("/"):
        message = "Your domain is not allowed to access this website."

        return message

    granted_scopes = r.json().get("scope").split(" ")

    if r.json().get("scope") == "" or any(scope not in granted_scopes for scope in required_scopes):
        message = f"You need to grant {', '.join(required_scopes).strip(', ')} access to use this tool."
        return message, None

    return None, r.json()


def is_authenticated(token_endpoint, headers, session, approved_user=None):
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
        access_token = headers.get("Authorization").split(" ")[-1]
    elif session.get("access_token"):
        access_token = session.get("access_token")
    else:
        return False

    check_token = requests.get(token_endpoint, headers={"Authorization": "Bearer " + access_token})

    if check_token.status_code != 200 or not check_token.json().get("me"):
        return False

    if approved_user is not None and check_token.status_code != 200 and check_token.json()["me"] != approved_user:
        return False

    return True

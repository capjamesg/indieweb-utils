import base64
import hashlib
import random
import string
from functools import wraps

from flask import Flask, flash, redirect, request, session
from flask_functions import AuthenticationError, indieauth_callback_handler

from ..webmentions.discovery import discover_endpoints


def discover_auth_endpoint_decorator(
    client_id: str, callback_url: str, required_scopes: list, domain: str, redirect_failed_destination: str
) -> Flask.Response:
    headers_to_find = ["authorization_endpoint", "token_endpoint"]

    headers = discover_endpoints(domain, headers_to_find)

    if not headers.get("authorization_endpoint"):
        flash("A valid IndieAuth authorization endpoint could not be found on your website.")
        return redirect(redirect_failed_destination)

    if not headers.get("token_endpoint"):
        flash("A valid IndieAuth token endpoint could not be found on your website.")
        return redirect(redirect_failed_destination)

    authorization_endpoint = headers.get("authorization_endpoint")
    token_endpoint = headers.get("token_endpoint")

    session["server_url"] = headers.get("microsub")

    random_code = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))

    session["code_verifier"] = random_code
    session["authorization_endpoint"] = authorization_endpoint
    session["token_endpoint"] = token_endpoint

    sha256_code = hashlib.sha256(random_code.encode("utf-8")).hexdigest()

    code_challenge = base64.b64encode(sha256_code.encode("utf-8")).decode("utf-8")

    state = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    session["state"] = state

    return redirect(
        authorization_endpoint
        + "?client_id="
        + client_id
        + "&redirect_uri="
        + callback_url
        + "&scope=profile&response_type=code&code_challenge="
        + code_challenge
        + "&code_challenge_method=S256&state="
        + state
        + "&scope={}".format(" ".join(required_scopes))
        + "&me="
        + domain
    )


def indieauth_callback_response(
    callback_url: str,
    client_id: str,
    me: str,
    required_scopes: list,
    redirect_success_destination: str,
    redirect_failed_destination: str,
) -> Flask.Response:
    code = request.args.get("code")
    state = request.args.get("state")

    try:
        response = indieauth_callback_handler(
            code=code,
            state=state,
            token_endpoint=session.get("token_endpoint"),
            code_verifier=session["code_verifier"],
            session_state=session.get("state"),
            callback_url=callback_url,
            client_id=client_id,
            me=me,
            required_scopes=required_scopes,
        )
    except AuthenticationError:
        flash("There was an error during authentication.")
        return redirect(redirect_failed_destination)

    session.pop("code_verifier")

    session["me"] = response.response.get("me")
    session["access_token"] = response.response.get("access_token")
    session["scope"] = response.response.get("scope")

    return redirect(redirect_success_destination)

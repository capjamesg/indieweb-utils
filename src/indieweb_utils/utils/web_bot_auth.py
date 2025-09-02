from http_message_signatures import (
    HTTPMessageSigner,
    HTTPMessageVerifier,
    HTTPSignatureKeyResolver,
    algorithms,
)
import requests
import base64
import random
import datetime


class HTTPSignatureKeyResolver(HTTPSignatureKeyResolver):
    def __init__(self, public_key_path: str, private_key_path: str):
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path

    def resolve_public_key(self, key_id: str):
        with open(self.public_key_path, "rb") as f:
            return f.read()

    def resolve_private_key(self, key_id: str):
        with open(self.private_key_path, "rb") as f:
            return f.read()


def signed_web_bot_auth_request(
    url: str, signature_agent: str, key_id: str, signature_key_resolver: HTTPSignatureKeyResolver
) -> requests.Response:
    """
    Make a signed request using the Web Bot Auth protocol.

    This function returns a requests.Response object.

    :param url: The URL to send the request to.
    :param signature_agent: The signature agent to use.
    :param key_id: The key ID to use for signing.
    :param key_resolver: The key resolver to use for signing.
    :return: The response from the request.

    .. code-block:: python

        from indieweb_utils import signed_web_bot_auth_request, HTTPSignatureKeyResolver

        key_resolver = HTTPSignatureKeyResolver(
            public_key_path="./public.pem",
            private_key_path="./private.pem"
        )

        response = signed_web_bot_auth_request(url, signature_agent, key_id, key_resolver)
    """
    request = requests.Request("GET", url)
    request = request.prepare()

    request.headers["Signature-Agent"] = signature_agent

    signer = HTTPMessageSigner(signature_algorithm=algorithms.ED25519, key_resolver=signature_key_resolver)
    signer.sign(
        request,
        key_id=key_id,
        nonce=base64.b64encode(random.randbytes(32)).decode(),
        expires=datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=10),
        tag="web-bot-auth",
        covered_component_ids=("@authority", "signature-agent"),
    )

    verifier = HTTPMessageVerifier(signature_algorithm=algorithms.ED25519, key_resolver=signature_key_resolver)
    if verifier.verify(request):
        response = requests.Session().send(request)

    return response

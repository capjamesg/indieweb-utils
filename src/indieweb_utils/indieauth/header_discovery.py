from dataclasses import dataclass

import requests

from ..webmentions.discovery import _discover_endpoints


@dataclass
class IndieAuthEndpoints:
    metadata_endpoint_found: bool = False
    issuer: str = None
    authorization_endpoint: str = None
    token_endpoint: str = None
    introspection_endpoint: str = None
    introspection_endpoint_auth_methods_supported: list = None
    revocation_endpoint: str = None
    revocation_endpoint_auth_methods_supported: list = None
    scopes_supported: list = None
    response_types_supported: list = None
    grant_types_supported: list = None
    service_documentation: str = None
    code_challenge_methods_supported: list = None
    authorization_response_iss_parameter_supported: bool = None
    userinfo_endpoint: str = None
    ticket_endpoint: str = None


def discover_indieauth_endpoints(url: str) -> IndieAuthEndpoints:
    """
    Discover and return the IndieAuth endpoints associated with a resource.

    :param url: The URL of the resource whose endpoints should be discovered.
    :type url: str
    :return: The IndieAuth endpoints associated with the resource.
    :rtype: IndieAuthEndpoints

    Example:

    .. code-block:: python

        import indieweb_utils

        endpoints = indieweb_utils.discover_indieauth_endpoints("https://jamesg.blog")

        print(endpoints.authorization_endpoint) # https://indieauth.com/auth

    :raises requests.exceptions.RequestException: If the request to the resource fails.
    """
    endpoints = _discover_endpoints(
        url, ["indieauth-metadata", "authorization_endpoint", "token_endpoint", "ticket_endpoint"]
    )

    if endpoints.get("indieauth-metadata"):
        try:
            response = requests.get(endpoints["indieauth-metadata"], timeout=5)
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Could not connect to the specified URL.")

        if response.status_code == 200:
            metadata = response.json()

            indieauth_endpoints = IndieAuthEndpoints(
                metadata_endpoint_found=True,
                issuer=metadata.get("issuer"),
                authorization_endpoint=metadata.get("authorization_endpoint"),
                token_endpoint=metadata.get("token_endpoint"),
                introspection_endpoint=metadata.get("introspection_endpoint"),
                introspection_endpoint_auth_methods_supported=metadata.get(
                    "introspection_endpoint_auth_methods_supported"
                ),
                revocation_endpoint=metadata.get("revocation_endpoint"),
                revocation_endpoint_auth_methods_supported=metadata.get("revocation_endpoint_auth_methods_supported"),
                scopes_supported=metadata.get("scopes_supported"),
                response_types_supported=metadata.get("response_types_supported"),
                grant_types_supported=metadata.get("grant_types_supported"),
                service_documentation=metadata.get("service_documentation"),
                code_challenge_methods_supported=metadata.get("code_challenge_methods_supported"),
                authorization_response_iss_parameter_supported=metadata.get(
                    "authorization_response_iss_parameter_supported"
                ),
                userinfo_endpoint=metadata.get("userinfo_endpoint"),
                ticket_endpoint=metadata.get("ticket_endpoint"),
            )

            return indieauth_endpoints
    else:
        return IndieAuthEndpoints(
            authorization_endpoint=endpoints.get("authorization_endpoint"),
            token_endpoint=endpoints.get("token_endpoint"),
            ticket_endpoint=endpoints.get("ticket_endpoint"),
        )

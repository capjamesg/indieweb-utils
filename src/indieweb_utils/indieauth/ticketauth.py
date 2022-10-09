import requests

from ..webmentions.discovery import _discover_endpoints


class TicketRedemptionError(Exception):
    """
    A ticket cannot be redeemed.
    """


class NoTokenEndpointFound(Exception):
    """
    A token endpoint is not present on the provided page.
    """


class NoTicketEndpointFound(Exception):
    """
    A ticket endpoint is not present on the provided page.
    """


class TicketCreationError(Exception):
    """
    A ticket cannot be created.
    """


def create_ticket(feed_url: str, ticket: str, subject: str, resource: str) -> None:
    """
    Create a ticket for an IndieAuth ticket server.

    """

    url_endpoints = _discover_endpoints(feed_url, ["ticket_endpoint"])

    if url_endpoints.get("ticket_endpoint") is None:
        raise NoTicketEndpointFound("A ticket endpoint was not found.")

    request_data = {"ticket": ticket, "resource": resource, "subject": subject}

    try:
        ticket_response = requests.post(url_endpoints["ticket_endpoint"], timeout=5, data=request_data)
    except requests.exceptions.RequestException:
        raise TicketCreationError("The ticket endpoint could not be accessed.")

    if ticket_response.status_code not in (200, 202):
        raise TicketCreationError("The ticket endpoint did not return a successful status code.")


def redeem_ticket(resource: str, ticket: str) -> str:
    """
    Redeem a ticket from an IndieAuth ticket server for an access token.
    """

    url_endpoints = _discover_endpoints(resource, ["token_endpoint"])

    if url_endpoints.get("token_endpoint") is None:
        raise NoTokenEndpointFound("A token endpoint was not found.")

    request_data = {"grant_type": "ticket", "ticket": ticket}

    try:
        ticket_response = requests.post(url_endpoints["token_endpoint"], timeout=5, data=request_data)
    except requests.exceptions.RequestException:
        raise TicketRedemptionError("The ticket endpoint could not be accessed.")

    if ticket_response.status_code != 200:
        raise TicketRedemptionError("The ticket endpoint returned a non-200 status code.")

    link_results = ticket_response.json()

    return link_results.json()["ticket"]

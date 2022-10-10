TicketAuth Features (Experimental)
==================================

IndieWeb Utils has experimental helper functions for the "Issue an access token" scetion of the TicketAuth draft specification.

While the TicketAuth specification is a draft, there are implementations following the specification.

The mechanics of these functions may change as TicketAuth becomes a more mature specification.

Send a IndieAuth ticket to a server
-----------------------------------

The `send_ticket()` function discovers the ticket endpoint of a subject and makes a POST request to their ticket endpoint.

This POST request contains an `application/x-www-form-urlencoded` payload with ticket, resource, and subject values. These are defined in Step 2 of the TicketAuth specification.

This function will return nothing if the POST request was successful. This is because a ticket endpoint does not return any value when the POST request is made. If the request fails, this function will raise an exception.

Redeem a ticket for an access token
-----------------------------------

The `redeem_ticket()` function redeems a ticket for an access token from a ticket endpoint.
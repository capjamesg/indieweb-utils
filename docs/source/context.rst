Generate Reply Context
------------------------

To generate reply context for a given page, use the following function:

.. autofunction:: indieweb_utils.get_reply_context

This function returns a ReplyContext object that looks like this:

.. autoclass:: indieweb_utils.ReplyContext

Generate a URL Summary
----------------------

You can generate a summary of a URL without retrieving the page using the `get_url_summary` function.

By default, this function can generate a summary for the following URLs:

- github.com
- twitter.com
- eventbrite.com / eventbrite.co.uk
- upcoming.com
- calagator.com
- events.indieweb.org
- indieweb.org

.. autofunction:: indieweb_utils.get_url_summary

You can specify custom mappings for other domains using the `custom_mappings` parameter.

This parameter accepts a dictionary of with domain names mapped to lists of tuples with patterns to match and strings to return, like this:

.. code-block:: python

    {
        "example.com": [
            (r"example.com/(\d+)", "Example #{}"),
        ]
    }

If a summary cannot be generated, this function returns "A post by [domain_name].", where domain name is the domain of the URL you passed into the function.


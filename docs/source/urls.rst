URLs
====

Canonicalize a URL
------------------------

Canonicalization turns a relative URL into a complete URL.

To canonicalize a URL, use this function:

.. autofunction:: indieweb_utils.canonicalize_url

This function returns a URL with a protocol, host, and path.

The domain of the resource is needed so that it can be added to the URL during canonicalization if the URL is relative.

A complete URL returned by this function looks like this:

.. code-block:: python

    https://indieweb.org/POSSE

Add hashtags and person tags to a string
-----------------------------------------

The `autolink_tags()` function replaces hashtags (#) with links to tag pages on a specified site. It also replaces person tags (ex. @james) with provided names and links to the person's profile.

This function is useful for enriching posts.

To use this function, pass in the following arguments:

.. autofunction:: indieweb_utils.autolink_tags

This function will only substitute tags in the list of tags passed through to this function if a `tags` value is provided. This ensures that the function does not create links that your application cannot resolve.

If you do not provide a `tags` value, the function will create links for all hashtags, as it is assumed that your application can resolve all hashtags.

`Tagging people <https://indieweb.org/person-tag>`_ is enabled by providing a dictionary with information on all of the people to whom you can tag.

If a person in an @ link is not in the tag dictionary, this function will not substitute that given @ link.

Here is an example value for a person tag database:

.. code-block:: python

    {
        "james": (
            "James' Coffee Blog",
            "https://jamesg.blog/""
        )
    }

This function maps the `@james` tag with the name "James' Coffee Blog" and the URL "https://jamesg.blog/". More people can be added as keys to the dictionary.

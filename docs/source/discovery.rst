Discovery
==========

Indieweb utils provides a number of functions to help you determine properties from webpages.


Find an article author
------------------------------------

You can discover the original author of an article as per the Authorship Specification.

To do so, use this function:

.. autofunction:: indieweb_utils.discover_author

Here are the arguments you can use:

- `url`: The URL of the web page whose author you want to discover.
- `page_contents`: The unmodified HTML of a web page whose author you want to discover.

The page_contents argument is optional.

If no page_contents argument is specified, the URL you stated is retrieved. Then, authorship inference begins.

If you specify a page_contents value, the HTML you parsed is used for authorship discovery. This saves on a HTML request if you have already retrieved the HTML for another reason (for example, if you need to retreive other values in the page HTML). You still need to specify a URL even if you specify a page_contents value.

The discover_author function can return one of two values:

- An author name (i.e. "James").
- The h-card of an author.

These are the two outputs defined in the authorship inference algorithm. Your program should be able to handle both of these outputs.

This code returns the following h-card:

.. code-block:: python

    {
        'type': ['h-card'],
        'properties': {
            'url': ['https://aaronparecki.com/'],
            'name': ['Aaron Parecki'],
            'photo': ['https://aaronparecki.com/images/profile.jpg']
        },
        'value': 'https://aaronparecki.com/'
    }


Find a post type
------------------------

To find the post type associated with a web page, you can use the `get_post_type` function.

The `get_post_type` function function uses the following syntax:

.. autofunction:: indieweb_utils.get_post_type

This function returns a single string with the post type of the specified web page.

See the `Post Type Discovery specification <https://indieweb.org/post-type-discovery>`_ for a full list of post types.


Custom Properties
------------------------

The structure of the custom properties tuple is:

.. code-block:: python

   (attribute_to_look_for, value_to_return)

An example custom property value is:

.. code-block:: python

    custom_properties = [
        ("poke-of", "poke")
    ]

This function would look for a poke-of attribute on a web page and return the "poke" value.

By default, this function contains all of the attributes in the Post Type Discovery mechanism.

Custom properties are added to the end of the post type discovery list, just before the "article" property. All specification property types are checked before your custom attribute.


Find the original version of a post
------------------------------------

To find the original version of a post per the Original Post Discovery algorithm, use this code:

.. autofunction:: indieweb_utils.discover_original_post

This function returns the URL of the original version of a post, if one is found. Otherwise, None is returned.


Find all feeds on a page
-----------------------------

To discover the feeds on a page, use this function:

.. autofunction:: indieweb_utils.discover_web_page_feeds

This function returns a list with all feeds on a page.

Each feed is structured as a FeedUrl object. FeedUrl objects contain the following attributes:

.. autoclass:: indieweb_utils.FeedUrl

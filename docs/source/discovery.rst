Discovery
==========

Indieweb utils provides a number of functions to help you determine properties from webpages.

Discover IndieWeb endpoints
---------------------------

The `discover_endpoints()` function parses HTTP Link headers and HTML `<link>` tags to find the specified endpoints.

.. autofunction:: indieweb_utils.discover_endpoints

This function only returns the specified endpoints if they can be found. It does not perform any validation to check that the discovered endpoints are valid URLs.

We recommend using the `discover_webmention_endpoint <https://indieweb-utils.readthedocs.io/en/latest/webmention.html#discover-a-webmention-endpoint>`_ function to discover webmention endpoints as this performs additional validation useful in webmention endpoint discovery.

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


Get a Representative h-card
---------------------------

To find the h-card that is considered representative of a web resource per the
`Representative h-card Parsing Algorithm <https://microformats.org/wiki/representative-h-card-parsing>`_,
use the following function:

.. autofunction:: indieweb_utils.get_representative_h_card

This function returns a dictionary with the h-card found on a web page.

Get a Page h-feed
---------------------------

The `discover_h_feed()` function implements the proposed `microformats2 h-feed discovery algorithm <https://microformats.org/wiki/h-feed#Discovery>`_.

This function looks for a h-feed on a given page. If one is not found, the function looks for a rel tag to a h-feed. If one is found, that document is parsed.

If a h-feed is found on the related document, the h-feed is returned.

This function returns a dictionary with the h-card found on a web page.

.. autofunction:: indieweb_utils.discover_h_feed
    
Infer the Name of a Page
------------------------

To find the name of a page per the `Page Name Discovery Algorithm <https://indieweb.org/page-name-discovery>`_, use this function:

.. autofunction:: indieweb_utils.get_page_name

This function searches:

1. For a h-entry title. If one is found, it is returned;
2. For a h-entry summary. If one is found, it is returned;
3. For a HTML page <title> tag. If one is found, it is returned;

Otherwise, this function returns "Untitled".

Get all URLs a Post Replies To
------------------------------

To find all of the URLs to which a reply post is replying, use this function:

.. autofunction:: indieweb_utils.get_reply_urls

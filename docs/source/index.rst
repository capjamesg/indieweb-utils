Welcome to IndieWeb Utils documentation!
=================================================

**indieweb-utils** is a Python library that provides building blocks for people implementing IndieWeb applications.
This library also contains implementations for some specifications that may be useful in IndieWeb applications.

To install IndieWeb Utils, use this command:

.. code-block:: bash

   pip3 install indieweb-utils

You can import the package using the following line of code:

.. code-block:: python

    import indieweb_utils

Below, you will find links to all of the methods available in IndieWeb Utils.
   
This project is licensed under an MIT license.

Contents
--------

.. toctree::

   usage
   discovery
   urls
   context
   indieauth
   webmention
   trackback
   rsd
   changelog

Feature Set
----------------

This package provides functions that cater to the following needs:

- Generating reply context for a given page.
- Finding the original version of a post per the `Original Post Discovery <https://indieweb.org/original-post-discovery#Algorithm>`_ specification.
- Finding the post type per the `Post Type Discovery <https://ptd.spec.indieweb.org/>`_ W3C note.
- Finding the `webmention endpoint on a page <https://webmention.net/draft/#sender-discovers-receiver-webmention-endpoint>`_, if one is provided.
- Canonicalizing a URL.
- Discovering the author of a post per the `Authorship <https://indieweb.org/authorship-spec>`_ Specification.
- Handling the response from an IndieAuth callback request.

If any of the above use cases resonate with you, this library may be helpful. Please note this library does not fully implement all IndieWeb specifications.

Rather, this library provides a set of building blocks that you can use to speed up your development of IndieWeb applications.

Here are a few of the many applications that may benefit from the functions provided in this library:

- `Micropub <https://indieweb.org/Micropub>`_ server.
- `Microsub <https://indieweb.org/Microsub>`_ server.
- `Webmention <https://indieweb.org/Webmention>`_ sender.
- Any application that needs to canonicalize a URL.
- An application implementing `IndieAuth authentication <https://indieweb.org/IndieAuth>`_.
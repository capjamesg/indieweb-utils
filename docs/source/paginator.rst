Paginating a list of posts
==========================

The `Paginator` class creates a generator that yields a list of posts for each page, where the length of each page is passed in when configuring the paginator.

This class is useful for building paginated lists of posts, such as a list of posts for a given month or year or for a category of content.

.. autoclass:: indieweb_utils.Paginator
   :members:
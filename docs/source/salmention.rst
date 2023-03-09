Salmention Features
===================

The `process_salmention()` function accepts two versions of a page: the page stored by a Webmention endpoint, and the current page.

The function compares the old and new versions of the page, looking for specified h-* objects. If it finds any, they will be added to a list.

All responses in _both_ the old and new page version are sent a Webmention notifying them that the source page has a new response.

The function returns:

1. A list of all the new mentions that were added to the page;
2. The Webmentions sent by the function and;
3. A list of all the mentions that were removed from the page.

.. autofunction:: indieweb_utils.process_salmention

There are two pre-defined helper constants that you can pass in the `supported_types`_ parameter of the `receive_salmention()` function:

- `indieweb_utils.salmention.salmention.SUPPORTED_TYPES`_ - All supported types of mentions
- `indieweb_utils.salmention.salmention.EXPANDED_SUPPORTED_TYPES`_ - All supported types of mentions except replies
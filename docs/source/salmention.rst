Salmention Features
===================

The `receive_salmention()` function checks for new and removed mentions from a post and sends Webmentions to every URL informing them of a new mention. This is an implementation of the `Salmention <https://indieweb.org/Salmention>`_ protocol.

The function requires the HTML markup of a page before and after a mention is sent so that comparisons can be made.

.. autofunction:: indieweb_utils.receive_salmention

There are two pre-defined helper constants that you can pass in the `supported_types`_ parameter of the `receive_salmention()` function:

- `indieweb_utils.salmention.send.SUPPORTED_TYPES`_ - All supported types of mentions
- `indieweb_utils.salmention.send.EXPANDED_SUPPORTED_TYPES`_ - All supported types of mentions except replies
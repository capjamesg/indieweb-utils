from indieweb_utils.salmention import receive_salmention


class TestSalmention:
    def test_receive_salmention(self):
        """Get reply context for a page on jamesg.blog."""

        # get new html as salmention_page.html fixture

        with open("tests/fixtures/salmention_page.html") as f:
            salmention_page = f.read()

        posts, sent_webmentions, deleted_posts = receive_salmention("", salmention_page)

        assert len(posts) == 1
        assert len(sent_webmentions["success"]) == 1
        assert len(deleted_posts) == 0

    def test_receive_salmention(self):
        """Get reply context for a page on jamesg.blog."""

        # get new html as salmention_page.html fixture

        with open("tests/fixtures/salmention_page.html") as f:
            salmention_page = f.read()

        posts, sent_webmentions, deleted_posts = receive_salmention("", salmention_page)

        assert len(posts) == 1
        assert len(sent_webmentions["success"]) == 1
        assert len(deleted_posts) == 0

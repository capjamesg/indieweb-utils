from indieweb_utils.replies import context


class TestReplyContext:
    def test_reply_context(self):
        reply_context = context.get_reply_context(
            url="https://jamesg.blog/2022/01/28/integrated-indieweb-services/"
        )

        assert reply_context.post_url == "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"
        assert reply_context.authors[0].url == "https://jamesg.blog"
        assert reply_context.authors[0].name == "James"
        assert reply_context.authors[0].photo == ""
        assert reply_context.webmention_endpoint == "https://webmention.jamesg.blog/endpoint"
        assert reply_context.photo == "https://jamesg.blog/assets/latte_1.jpeg"
        assert reply_context.name == "Integrated IndieWeb Services"
        assert reply_context.video == ""
        assert reply_context.post_html
        assert reply_context.post_text

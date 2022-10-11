import responses

from indieweb_utils.replies import context


class TestReplyContext:
    @responses.activate
    def test_reply_context_1(self):
        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"
        with open("tests/fixtures/reply1.html") as f:
            responses.add(responses.Response(responses.GET, url=url, body=f.read()))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.authors[0].url == "https://jamesg.blog"
        assert reply_context.authors[0].name == "James"
        assert reply_context.authors[0].photo == ""
        assert reply_context.webmention_endpoint == "https://webmention.jamesg.blog/endpoint"
        assert reply_context.photo == "https://jamesg.blog/assets/latte_1.jpeg"
        assert reply_context.name == "Integrated IndieWeb Services"
        assert reply_context.video == ""
        assert reply_context.post_html
        assert reply_context.post_text

    @responses.activate
    def test_reply_context_2(self):
        url = "https://aaronparecki.com/2022/01/29/12/raspi-usb-webcam-hdmi"
        author_url = "https://aaronparecki.com/"
        with open("tests/fixtures/reply2.html") as f:
            responses.add(responses.Response(responses.GET, url=url, body=f.read()))

        with open("tests/fixtures/author2.html") as f:
            responses.add(responses.Response(responses.GET, url=author_url, body=f.read()))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == "https://webmention.io/aaronpk/webmention"
        assert reply_context.authors[0].url == author_url
        assert reply_context.authors[0].name == "Aaron Parecki"
        assert reply_context.authors[0].photo == "https://aaronparecki.com/images/profile.jpg"
        assert reply_context.video == ""
        assert reply_context.photo == ""
        assert reply_context.post_html
        assert reply_context.post_text

    @responses.activate
    def test_reply_context_3(self):
        url = (
            "https://www.theguardian.com/technology/2022/jan/31/"
            "beats-fit-pro-review-apple-workout-ready-airpods-pro-rivals-battery-price"
        )
        with open("tests/fixtures/reply3.html") as f:
            responses.add(responses.Response(responses.GET, url=url, body=f.read()))
        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == ""
        assert reply_context.authors[0].url == "https://www.theguardian.com"
        assert reply_context.authors[0].name == ""
        assert reply_context.authors[0].photo == ""
        assert reply_context.video == ""
        assert (
            reply_context.photo
            == "https://i.guim.co.uk/img/media/07916e0013c53049a2d399d83753697621d01ab9/494_0_4962_2977/master/4962.jpg?width=1200&height=630&quality=85&auto=format&fit=crop&overlay-align=bottom%2Cleft&overlay-width=100p&overlay-base64=L2ltZy9zdGF0aWMvb3ZlcmxheXMvdGctcmV2aWV3LTQucG5n&enable=upscale&s=48a3cfbf6e6479f9f631b1852e1875b6"  # noqa
        )
        assert reply_context.post_html
        assert reply_context.post_text

    @responses.activate
    def test_reply_context_4(self):
        url = "https://warmedal.se/~bjorn/posts/2022-01-30-collecting-reply-posts-for-posterity.html"
        with open("tests/fixtures/reply4.html") as f:
            responses.add(responses.Response(responses.GET, url=url, body=f.read()))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == ""
        assert reply_context.authors[0].url == "https://warmedal.se"
        assert reply_context.authors[0].name == ""
        assert reply_context.authors[0].photo == ""
        assert reply_context.video == ""
        assert reply_context.photo == ""
        assert reply_context.post_html
        assert reply_context.post_text

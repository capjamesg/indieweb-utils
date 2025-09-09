import responses
from indieweb_utils.replies import context


class TestReplyContext:
    @responses.activate
    def test_reply_context_1(self, reply1):
        """Get reply context for a page on jamesg.blog."""

        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"
        responses.add(responses.Response(responses.GET, url=url, body=reply1))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.authors[0].url == "https://jamesg.blog"
        assert reply_context.authors[0].name == "James"
        assert reply_context.authors[0].photo == ""
        assert reply_context.webmention_endpoint == "https://webmention.jamesg.blog/endpoint"
        assert reply_context.photo == "https://jamesg.blog/assets/latte_1.jpeg"
        assert reply_context.name == "Integrated IndieWeb Services"
        assert reply_context.video == ""
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None

    @responses.activate
    def test_reply_context_2(self, reply2, author2):
        """Get reply context for a page on aaronparecki.com."""
        url = "https://aaronparecki.com/2022/01/29/12/raspi-usb-webcam-hdmi"
        author_url = "https://aaronparecki.com/"

        responses.add(responses.Response(responses.GET, url=url, body=reply2))

        responses.add(responses.Response(responses.GET, url=author_url, body=author2))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == "https://webmention.io/aaronpk/webmention"
        assert reply_context.authors[0].url == author_url
        assert reply_context.authors[0].name == "Aaron Parecki"
        assert reply_context.authors[0].photo == "https://aaronparecki.com/images/profile.jpg"
        assert reply_context.video == ""
        assert reply_context.photo == ""
        assert (
            reply_context.description
            == "This post exists to collect my notes on displaying a USB webcam on the Raspberry Pi HDMI outputs. This is not the same as streaming the webcam (easy), and this is not for use with the Raspberry Pi camera module..."  # noqa: E501
        )
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None

    @responses.activate
    def test_reply_context_3(self, reply3):
        """Get reply context for a page on The Guardian."""
        url = (
            "https://www.theguardian.com/technology/2022/jan/31/"
            "beats-fit-pro-review-apple-workout-ready-airpods-pro-rivals-battery-price"
        )

        responses.add(responses.Response(responses.GET, url=url, body=reply3))
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
        assert (
            reply_context.description
            == "Good sound, noise cancelling and spatial audio, with six-hour battery, Android support and cheaper price"  # noqa: E501
        )
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None

    @responses.activate
    def test_reply_context_4(self, reply4):
        """Get reply context for a page on warmedal.se."""
        url = "https://warmedal.se/~bjorn/posts/2022-01-30-collecting-reply-posts-for-posterity.html"

        responses.add(responses.Response(responses.GET, url=url, body=reply4))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == ""
        assert reply_context.authors[0].url == "https://warmedal.se"
        assert reply_context.authors[0].name == ""
        assert reply_context.authors[0].photo == ""
        assert reply_context.video == ""
        assert reply_context.photo == ""
        assert reply_context.description == ""
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None

    @responses.activate
    def test_reply_context_5(self, reply5):
        """Get reply context for a page on beakerbrowser.com."""
        url = "https://beakerbrowser.com"

        responses.add(responses.Response(responses.GET, url=url, body=reply5))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == ""
        assert reply_context.authors[0].url == "https://beakerbrowser.com"
        assert reply_context.authors[0].name == ""
        assert reply_context.authors[0].photo == ""
        assert reply_context.name == "Beaker Browser"
        assert reply_context.video == "https://beakerbrowser.com/beaker-site-demo.mp4"
        assert reply_context.photo == "https://beakerbrowser.com/img/logo/logo.png"
        assert (
            reply_context.description
            == "Beaker is a new peer-to-peer browser for a Web where users control their data and websites are hosted locally."  # noqa
        )
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None

    @responses.activate
    def test_reply_context_6(self, reply6):
        """Get reply context for a page on w3c.org."""
        url = "https://www.w3.org/community/sustyweb/"

        responses.add(responses.Response(responses.GET, url=url, body=reply6))

        reply_context = context.get_reply_context(url=url)

        assert reply_context.webmention_endpoint == ""
        assert reply_context.authors[0].url == "https://www.w3.org"
        assert reply_context.authors[0].name == ""
        assert reply_context.authors[0].photo == ""
        assert reply_context.name == "Sustainable Web Design Community Group"
        assert reply_context.video == ""
        assert (
            reply_context.photo
            == "https://www.w3.org/community/src/templates/wordpress/StoryTeller/img/cgbg-logo.png"  # noqa
        )
        assert reply_context.post_html is not None
        assert reply_context.post_text is not None
        assert (
            reply_context.description
            == "A community group dedicated to creating sustainable websites. This group will not publish specifications."  # noqa
        )

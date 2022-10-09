import pytest
import responses


class TestInReplyToAlgorithm:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_reply_urls

        return get_reply_urls

    def test_in_reply_to_algorithm(self, target, in_reply_to):
        url = "https://aaronparecki.com/2022/09/29/29/"

        responses.add(
            responses.Response(
                method="GET",
                url=url,
                body=in_reply_to,
            )
        )

        expected_urls = ["https://twitter.com/photojoseph/status/1575682059502174210?s=12"]

        results = target(url, html=in_reply_to)

        for url in results:
            assert url in expected_urls

        assert len(expected_urls) == len(results)

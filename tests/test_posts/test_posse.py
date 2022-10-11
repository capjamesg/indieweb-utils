import pytest
import responses


class TestPostTypeDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_syndicated_copies

        return get_syndicated_copies

    @responses.activate
    def test_get_syndicated_copies(self, target):
        url = "https://aaronparecki.com/2022/09/26/18/eyefi"
        with open("tests/fixtures/post.html") as f:
            responses.add(responses.Response(responses.GET, url=url, body=f.read()))

        syndicated_copies = target(url=url)

        expected_syndicated_copies = [
            "https://twitter.com/aaronpk/status/1574593963033600005",
            "https://micro.blog/aaronpk/13432950",
        ]

        for syndicated_copy in syndicated_copies:
            assert syndicated_copy in expected_syndicated_copies

        assert len(syndicated_copies) == len(expected_syndicated_copies)

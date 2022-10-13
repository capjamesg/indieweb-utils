import pytest
import responses


class TestPostTypeDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_syndicated_copies

        return get_syndicated_copies

    @responses.activate
    def test_get_syndicated_copies(self, target, post):
        """Test the get_syndicated_copies algorithm to find the URLs to which a post was syndicated."""
        url = "https://aaronparecki.com/2022/09/26/18/eyefi"

        responses.add(responses.Response(responses.GET, url=url, body=post))

        syndicated_copies = target(url=url)

        expected_syndicated_copies = [
            "https://twitter.com/aaronpk/status/1574593963033600005",
            "https://micro.blog/aaronpk/13432950",
        ]

        for syndicated_copy in syndicated_copies:
            assert syndicated_copy in expected_syndicated_copies

        assert len(syndicated_copies) == len(expected_syndicated_copies)

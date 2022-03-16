import pytest
import responses


class TestRelMeAuthLinkDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_valid_relmeauth_links

        return get_valid_relmeauth_links

    def test_rel_me_auth_link_discovery(self, target, index):
        # NOTE: This test will take a few seconds as it executes multiple requests.
        url = "https://jamesg.blog"

        responses.add(responses.Response(method="GET", url=url, body=index))

        assert target(url) == ["https://indieweb.social/@capjamesg"]

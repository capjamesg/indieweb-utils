import pytest


class TestRelMeAuthLinkDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_valid_relmeauth_links

        return get_valid_relmeauth_links

    def test_rel_me_auth_link_discovery(self, target):
        # NOTE: This test will take a few seconds as it executes multiple requests.
        url = "https://jamesg.blog"

        links = target(url)

        assert links == [
            "https://indieweb.social/@capjamesg"
        ]

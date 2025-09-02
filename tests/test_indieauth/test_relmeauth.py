import pytest
import responses


class TestRelMeAuthLinkDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_valid_relmeauth_links

        return get_valid_relmeauth_links

    @responses.activate
    def test_rel_me_auth_link_discovery(self, target, index):
        """Test discovery of rel=me links on a web page."""
        url = "https://jamesg.blog"

        responses.add(responses.Response(responses.GET, url=url, body=index, status=200))

        expected_responses = [
            "https://indieweb.social/@capjamesg",
            "https://micro.blog/capjamesg",
            "https://jamesg.coffee",
            "https://www.instagram.com/capjamesg/",
            "https://indieweb.org/User:Jamesg.blog",
            "https://github.com/capjamesg",
            "https://jamesg.blog/assets/key.asc",
            "mailto:jamesg@jamesg.blog",
        ]

        results = target(url, html=index, require_rel_me_link_back=False)

        for r in expected_responses:
            if r not in results:
                raise AssertionError(f"Expected {r} to be in {results}")

        assert len(expected_responses) == len(results)

import pytest
import responses


class TestRelMeAuthLinkDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_valid_relmeauth_links

        return get_valid_relmeauth_links

    def test_rel_me_auth_link_discovery(self, target):
        url = "https://jamesg.blog"

        with open("tests/fixtures/index.html") as f:
            file_contents = f.read()
            responses.add(responses.Response(responses.GET, url=url, body=file_contents))

            expected_responses = [
                "https://indieweb.org/User:Jamesg.blog",
                "https://indieweb.social/@capjamesg",
                "https://micro.blog/capjamesg",
                "https://jamesg.coffee/",
            ]

            results = target(url, html=file_contents, require_rel_me_link_back=False)

            for r in expected_responses:
                if r not in results:
                    raise AssertionError(f"Expected {r} to be in {results}")

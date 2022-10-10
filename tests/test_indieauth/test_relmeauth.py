import pytest
import responses


class TestRelMeAuthLinkDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_valid_relmeauth_links

        return get_valid_relmeauth_links

    @responses.activate
    def test_rel_me_auth_link_discovery(self, target):
        url = "https://jamesg.blog"

        with open("tests/fixtures/index.html") as f:
            file_contents = f.read()
            responses.add(responses.Response(responses.GET, url=url, body=file_contents, status=200))

            expected_responses = [
                "https://indieweb.social/@capjamesg",
                "https://micro.blog/capjamesg",
                "https://jamesg.coffee/",
                "https://www.instagram.com/capjamesg/",
                "https://indieweb.org/User:Jamesg.blog",
                "https://github.com/capjamesg",
                "https://jamesg.blog/assets/key.asc",
                "mailto:jamesg@jamesg.blog",
            ]

            results = target(url, html=file_contents, require_rel_me_link_back=False)

            for r in expected_responses:
                if r not in results:
                    raise AssertionError(f"Expected {r} to be in {results}")

            assert len(expected_responses) == len(results)

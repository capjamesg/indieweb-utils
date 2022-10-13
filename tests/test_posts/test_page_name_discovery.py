import pytest
import responses


class TestPageNameDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_page_name

        return get_page_name

    @responses.activate
    def test_page_name_discovery(self, target, reply1):
        """Test page name discovery algorithm and ensure it returns the name of a page."""
        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"

        responses.add(
            responses.Response(
                method="GET",
                url=url,
                body=reply1,
            )
        )

        assert target(url) == "Integrated IndieWeb Services"

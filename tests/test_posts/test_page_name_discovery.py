import pytest
import responses


class TestPageNameDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_page_name

        return get_page_name

    @responses.activate
    def test_page_name_discovery(self, target):
        url = "https://jamesg.blog/2022/01/28/integrated-indieweb-services/"

        with open("tests/fixtures/reply1.html") as f:
            responses.add(
                responses.Response(
                    method="GET",
                    url=url,
                    body=f.read(),
                )
            )

        assert target(url) == "Integrated IndieWeb Services"

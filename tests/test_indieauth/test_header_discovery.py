import pytest
import responses


class TestHeaderDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils.indieauth.header_discovery import (
            discover_indieauth_endpoints,
        )

        return discover_indieauth_endpoints

    def test_header_discovery(self, target, index):
        url = "https://jamesg.blog"

        responses.add(responses.Response(method="GET", url=url, body=index))

        endpoints = target(url)

        assert endpoints.authorization_endpoint == "https://indieauth.com/auth"
        assert endpoints.token_endpoint == "https://tokens.indieauth.com/token"
        assert endpoints.ticket_endpoint == None
        assert endpoints.metadata_endpoint_found == False

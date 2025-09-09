import pytest
import responses


class TestHeaderDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils.indieauth.header_discovery import \
            discover_indieauth_endpoints

        return discover_indieauth_endpoints

    @responses.activate
    def test_header_discovery_no_metadata(self, target, index):
        url = "https://jamesg.blog"

        responses.add(responses.Response(method="GET", url=url, body=index))

        endpoints = target(url)

        assert endpoints.authorization_endpoint == "https://auth.jamesg.blog/auth"
        assert endpoints.token_endpoint == "https://auth.jamesg.blog/token"
        assert endpoints.ticket_endpoint is None
        assert endpoints.metadata_endpoint_found is False

    @responses.activate
    def test_header_discovery_with_metadata(self, target, index):
        url = "https://aaronparecki.com"

        with open("tests/fixtures/author2.html") as f:
            responses.add(responses.Response(method="GET", url=url, body=f.read()))

        with open("tests/fixtures/auth_server.json") as f:
            responses.add(
                responses.Response(
                    method="GET", url="https://aaronparecki.com/.well-known/oauth-authorization-server", body=f.read()
                )
            )

        endpoints = target(url)

        assert endpoints.metadata_endpoint_found is True
        assert endpoints.issuer == "https://aaronparecki.com/"
        assert endpoints.authorization_endpoint == "https://aaronparecki.com/auth"
        assert endpoints.token_endpoint == "https://aaronparecki.com/auth/token"
        assert endpoints.ticket_endpoint is None
        assert endpoints.introspection_endpoint == "https://aaronparecki.com/auth/introspect"
        assert endpoints.introspection_endpoint_auth_methods_supported == ["none"]
        assert endpoints.revocation_endpoint == "https://aaronparecki.com/auth/token/revoke"
        assert endpoints.revocation_endpoint_auth_methods_supported == ["none"]
        assert endpoints.scopes_supported == [
            "profile",
            "email",
            "create",
            "draft",
            "update",
            "delete",
            "media",
            "read",
            "follow",
            "mute",
            "block",
            "channels",
        ]
        assert endpoints.response_types_supported is None
        assert endpoints.grant_types_supported is None
        assert endpoints.service_documentation == "https://indieauth.spec.indieweb.org/"
        assert endpoints.code_challenge_methods_supported == ["S256"]
        assert endpoints.authorization_response_iss_parameter_supported is True
        assert endpoints.userinfo_endpoint == "https://aaronparecki.com/auth/userinfo"

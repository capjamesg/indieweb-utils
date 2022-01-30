from indieweb_utils.indieauth import server


class TestGenerateAuthToken:
    def test_generate_auth_token(self):
        """A end-to-end happy path test to confirm the entire indieauth flow is working properly.
         It will: generate an auth token, redeem the token, validate access, and validate authorization.
        """

        response = server.generate_auth_token(
            me="https://example.com/me",
            client_id="https://example.com/client",
            redirect_uri="https://example.com/redirect",
            response_type="code",
            state="test_state",
            code_challenge_method="S256",
            final_scope="read write",
            secret_key="test_secret_key"
        )

        assert response.code
        assert response.code_verifier
        assert response.code_challenge

        exchange_response = server.redeem_code(
            grant_type="authorization_code",
            code=response.code,
            redirect_uri="https://example.com/redirect",
            client_id="https://example.com/client",
            code_verifier=response.code_verifier,
            secret_key="test_secret_key"
        )

        assert exchange_response.access_token
        assert exchange_response.token_type == "bearer"
        assert exchange_response.scope == "read write"
        assert exchange_response.me == "https://example.com/me"
    
        validate_response = server.validate_access_token(
            authorization_code=exchange_response.access_token,
            secret_key="test_secret_key"
        )

        assert validate_response.me == "https://example.com/me"
        assert validate_response.client_id == "https://example.com/client"
        assert validate_response.scope == "read write"
        assert validate_response.decoded_authorization_code

        validate_auth_response = server.validate_authorization_response(
            grant_type="authorization_code",
            code="12345",
            client_id="https://jamesg.blog",
            redirect_uri="https://jamesg.blog/authorize",
            code_challenge=response.code_challenge,
            code_challenge_method="S256",
            allowed_methods=["S256"]
        )

        assert validate_auth_response is True

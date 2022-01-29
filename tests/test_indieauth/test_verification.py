import time
import pytest

from indieweb_utils.indieauth import server


class TestGenerateAuthToken:
    def test_generate_auth_token(self):
        """Test function to generate an authentication token."""

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
    

# class TestAuthorizationResponseValidation:
#     def test_authorization_response_validation(self):
#         assert validate_authorization_response(
#             grant_type="authorization_code",
#             code="12345",
#             client_id="https://jamesg.blog",
#             redirect_uri="https://jamesg.blog/authorize",
#             code_challenge="12345",
#             code_challenge_method="S256",
#             allowed_methods=["S256"]
#         ) == TokenValidationError


# class TestVerifyDecodedCode:
#     def test_verify_decoded_code(self):
#         assert verify_decoded_code(
#             client_id="https://jamesg.blog",
#             redirect_uri="https://jamesg.blog/authorize",
#             decoded_client_id="https://jamesg.blog",
#             decoded_redirect_uri="https://jamesg.blog/authorize",
#             decoded_expires=int(time.time()) + 3600
#         ) == True

# import time
# import pytest

# from indieweb_utils import validate_authorization_response, verify_decoded_code, \
#     TokenValidationError


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
"""Tests for the Users service."""

from __future__ import annotations

from nuvei.services.users import GET_USER_CHECKSUM_FIELDS, USER_CHECKSUM_FIELDS


class TestCreateUser:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.users.create_user(
            userTokenId="user_tok_1", countryCode="US",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "createUser"

    def test_includes_checksum(self, client, mock_request):
        client.users.create_user(
            userTokenId="user_tok_1", countryCode="US",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data

    def test_passes_optional_fields(self, client, mock_request):
        client.users.create_user(
            userTokenId="user_tok_1", countryCode="US",
            firstName="John", lastName="Doe",
            email="john@example.com", phone="555-1234",
        )
        _, data = mock_request.call_args[0]
        assert data["firstName"] == "John"
        assert data["lastName"] == "Doe"
        assert data["email"] == "john@example.com"


class TestUpdateUser:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.users.update_user(
            userTokenId="user_tok_1", firstName="Jane",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "updateUser"


class TestGetUserDetails:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.users.get_user_details(userTokenId="user_tok_1")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getUserDetails"

    def test_includes_checksum(self, client, mock_request):
        client.users.get_user_details(userTokenId="user_tok_1")
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestUserChecksumFields:
    def test_user_checksum_fields(self):
        assert USER_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "firstName", "lastName", "address", "state", "city", "zip",
            "countryCode", "phone", "locale", "email", "county",
            "timeStamp", "secretKey",
        ]

    def test_get_user_checksum_fields(self):
        assert GET_USER_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

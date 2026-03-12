"""Tests for the Nuvei client (sync)."""

from __future__ import annotations

import pytest

from nuvei import Nuvei
from nuvei.exceptions import APIError, AuthenticationError


@pytest.fixture
def client():
    c = Nuvei(
        merchant_id="test_merchant",
        merchant_site_id="12345",
        merchant_secret_key="secret_key_here",
        environment="test",
    )
    yield c
    c.close()


class TestClientInit:
    def test_attributes(self, client: Nuvei):
        assert client.merchant_id == "test_merchant"
        assert client.merchant_site_id == "12345"
        assert client.algorithm == "sha256"
        assert client.server_config.environment.value == "test"

    def test_service_accessors(self, client: Nuvei):
        assert client.authentication is not None
        assert client.payments is not None
        assert client.financial is not None
        assert client.three_d_secure is not None
        assert client.card_operations is not None
        assert client.users is not None
        assert client.user_payment_options is not None
        assert client.subscriptions is not None
        assert client.orders is not None
        assert client.advanced_apm is not None

    def test_source_application_default(self, client: Nuvei):
        assert client.source_application == "PYTHON_SDK"

    def test_session_token_caching(self, client: Nuvei):
        assert client.session_token is None
        client._cache_session_token({"sessionToken": "cached_abc"})
        assert client.session_token == "cached_abc"


class TestInjectCredentials:
    def test_injects_all_fields(self, client: Nuvei):
        data = client._inject_credentials({})
        assert data["merchantId"] == "test_merchant"
        assert data["merchantSiteId"] == "12345"
        assert "clientRequestId" in data
        assert "timeStamp" in data
        assert len(data["timeStamp"]) == 14
        assert data["sourceApplication"] == "PYTHON_SDK"

    def test_does_not_overwrite_existing(self, client: Nuvei):
        data = client._inject_credentials({"merchantId": "custom"})
        assert data["merchantId"] == "custom"


class TestSign:
    def test_adds_checksum(self, client: Nuvei):
        fields = ["merchantId", "merchantSiteId", "clientRequestId", "timeStamp", "secretKey"]
        data = client._sign({}, fields)
        assert "checksum" in data
        assert len(data["checksum"]) == 64  # SHA-256 hex


class TestHandleResponse:
    def test_success_passthrough(self):
        body = {"errCode": 0, "status": "SUCCESS", "sessionToken": "abc"}
        result = Nuvei._handle_response(body, "getSessionToken")
        assert result["sessionToken"] == "abc"

    def test_error_raises_api_error(self):
        body = {"errCode": 1001, "status": "ERROR", "reason": "Invalid merchant"}
        with pytest.raises(APIError, match="Invalid merchant"):
            Nuvei._handle_response(body, "payment")

    def test_auth_error_raises_authentication_error(self):
        body = {"errCode": 1001, "status": "ERROR", "reason": "Bad credentials"}
        with pytest.raises(AuthenticationError, match="Bad credentials"):
            Nuvei._handle_response(body, "getSessionToken")


class TestContextManager:
    def test_with_statement(self):
        with Nuvei(
            merchant_id="m",
            merchant_site_id="s",
            merchant_secret_key="k",
            environment="test",
        ) as client:
            assert client.merchant_id == "m"

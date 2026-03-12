"""Tests for the Authentication service."""

from __future__ import annotations

from nuvei.services.authentication import SESSION_TOKEN_CHECKSUM_FIELDS


class TestGetSessionToken:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.get_session_token()
        mock_request.assert_called_once()
        endpoint, data = mock_request.call_args[0]
        assert endpoint == "getSessionToken"

    def test_injects_credentials(self, client, mock_request):
        client.get_session_token()
        _, data = mock_request.call_args[0]
        assert data["merchantId"] == "test_mid"
        assert data["merchantSiteId"] == "123456"
        assert "clientRequestId" in data
        assert "timeStamp" in data

    def test_includes_checksum(self, client, mock_request):
        client.get_session_token()
        _, data = mock_request.call_args[0]
        assert "checksum" in data
        assert len(data["checksum"]) == 64

    def test_passes_extra_kwargs(self, client, mock_request):
        client.get_session_token(clientUniqueId="uid-1")
        _, data = mock_request.call_args[0]
        assert data["clientUniqueId"] == "uid-1"

    def test_caches_session_token(self, client, mock_request):
        assert client.session_token is None
        client.get_session_token()
        assert client.session_token == "tok_abc123"

    def test_checksum_field_order(self):
        assert SESSION_TOKEN_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

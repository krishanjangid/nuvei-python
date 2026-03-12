"""Tests for the 3D Secure service."""

from __future__ import annotations

from nuvei.services.three_d_secure import (
    AUTHORIZE3D_CHECKSUM_FIELDS,
    DYNAMIC3D_CHECKSUM_FIELDS,
)


class TestAuthorize3d:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.three_d_secure.authorize3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {"threeD": {}}},
            relatedTransactionId="txn_init_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "authorize3d"

    def test_includes_checksum(self, client, mock_request):
        client.three_d_secure.authorize3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestVerify3d:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.three_d_secure.verify3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "verify3d"

    def test_no_checksum(self, client, mock_request):
        """verify3d uses _inject_credentials, no checksum."""
        client.three_d_secure.verify3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        _, data = mock_request.call_args[0]
        assert "checksum" not in data


class TestDynamic3D:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.three_d_secure.dynamic3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "dynamic3D"

    def test_includes_checksum(self, client, mock_request):
        client.three_d_secure.dynamic3d(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestThreeDSecureChecksumFields:
    def test_authorize3d_checksum_fields(self):
        assert AUTHORIZE3D_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "amount", "currency", "timeStamp", "secretKey",
        ]

    def test_dynamic3d_checksum_fields(self):
        assert DYNAMIC3D_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "amount", "currency", "timeStamp", "secretKey",
        ]

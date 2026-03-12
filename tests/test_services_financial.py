"""Tests for the Financial service."""

from __future__ import annotations

from nuvei.services.financial import (
    PAYOUT_CHECKSUM_FIELDS,
    PAYOUT_STATUS_CHECKSUM_FIELDS,
    REFUND_CHECKSUM_FIELDS,
    SETTLE_CHECKSUM_FIELDS,
    VOID_CHECKSUM_FIELDS,
)


class TestSettleTransaction:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.financial.settle_transaction(
            relatedTransactionId="txn_1", amount="50.00",
            currency="USD", authCode="auth_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "settleTransaction"

    def test_includes_checksum(self, client, mock_request):
        client.financial.settle_transaction(
            relatedTransactionId="txn_1", amount="50.00",
            currency="USD", authCode="auth_1",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data

    def test_passes_kwargs(self, client, mock_request):
        client.financial.settle_transaction(
            relatedTransactionId="txn_1", amount="50.00",
            currency="USD", authCode="auth_1",
            descriptorMerchantName="TestMerchant",
            comment="Partial settle",
        )
        _, data = mock_request.call_args[0]
        assert data["descriptorMerchantName"] == "TestMerchant"
        assert data["comment"] == "Partial settle"


class TestRefundTransaction:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.financial.refund_transaction(
            relatedTransactionId="txn_2", amount="10.00",
            currency="USD", clientUniqueId="ref-001",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "refundTransaction"


class TestVoidTransaction:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.financial.void_transaction(
            relatedTransactionId="txn_3", amount="100.00",
            currency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "voidTransaction"


class TestPayout:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.financial.payout(
            userTokenId="user_1", amount="25.00", currency="USD",
            userPaymentOption={"userPaymentOptionId": "upo_1"},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "payout"

    def test_includes_checksum(self, client, mock_request):
        client.financial.payout(
            userTokenId="user_1", amount="25.00", currency="USD",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestGetPayoutStatus:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.financial.get_payout_status(clientRequestId="cr_1")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getPayoutStatus"


class TestFinancialChecksumFields:
    def test_settle_checksum_fields(self):
        assert SETTLE_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
            "amount", "currency", "relatedTransactionId", "authCode",
            "descriptorMerchantName", "descriptorMerchantPhone", "comment",
            "urlDetails", "timeStamp", "secretKey",
        ]

    def test_refund_checksum_fields(self):
        assert REFUND_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
            "amount", "currency", "relatedTransactionId", "authCode",
            "comment", "urlDetails", "timeStamp", "secretKey",
        ]

    def test_void_checksum_fields(self):
        assert VOID_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
            "amount", "currency", "relatedTransactionId", "authCode",
            "comment", "urlDetails", "timeStamp", "secretKey",
        ]

    def test_payout_checksum_fields(self):
        assert PAYOUT_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "amount", "currency", "timeStamp", "secretKey",
        ]

    def test_payout_status_checksum_fields(self):
        assert PAYOUT_STATUS_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

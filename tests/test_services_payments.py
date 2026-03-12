"""Tests for the Payments service."""

from __future__ import annotations

from nuvei.services.payments import PAYMENT_CHECKSUM_FIELDS


class TestPaymentChecksumFields:
    def test_field_order(self):
        assert PAYMENT_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "amount", "currency", "timeStamp", "secretKey",
        ]


class TestPayment:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.payment(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "payment"

    def test_includes_checksum(self, client, mock_request):
        client.payments.payment(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data

    def test_passes_all_kwargs(self, client, mock_request):
        client.payments.payment(
            sessionToken="tok", amount="10.00", currency="USD",
            transactionType="Sale",
            paymentOption={"card": {"cardNumber": "4111111111111111"}},
            userTokenId="user_1", isRebilling="0",
        )
        _, data = mock_request.call_args[0]
        assert data["transactionType"] == "Sale"
        assert data["userTokenId"] == "user_1"
        assert data["isRebilling"] == "0"


class TestPaymentCC:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.payment_cc(
            sessionToken="tok", amount="5.00", currency="EUR",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "paymentCC"


class TestPaymentAPM:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.payment_apm(
            sessionToken="tok", amount="5.00", currency="EUR",
            paymentMethod="apmgw_Neteller",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "paymentAPM"


class TestInitPayment:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.init_payment(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "initPayment"

    def test_includes_checksum(self, client, mock_request):
        client.payments.init_payment(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestGetPaymentStatus:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.get_payment_status("tok_session")
        endpoint, data = mock_request.call_args[0]
        assert endpoint == "getPaymentStatus"
        assert data["sessionToken"] == "tok_session"

    def test_no_checksum(self, client, mock_request):
        """getPaymentStatus uses _inject_credentials, not _sign."""
        client.payments.get_payment_status("tok_session")
        _, data = mock_request.call_args[0]
        assert "checksum" not in data


class TestAccountCapture:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.account_capture(
            sessionToken="tok", userTokenId="u1",
            paymentMethod="apmgw_Neteller",
            currencyCode="USD", countryCode="US", amount="100",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "accountCapture"


class TestGetMcpRates:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.get_mcp_rates(
            sessionToken="tok", fromCurrency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getMcpRates"


class TestGetDccDetails:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.payments.get_dcc_details(
            sessionToken="tok", clientUniqueId="cu",
            originalAmount="100", originalCurrency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getDccDetails"

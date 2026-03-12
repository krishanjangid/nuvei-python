"""Tests for the Orders service."""

from __future__ import annotations

from nuvei.services.orders import ORDER_CHECKSUM_FIELDS, ORDER_DETAILS_CHECKSUM_FIELDS


class TestOpenOrder:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.orders.open_order(amount="100.00", currency="USD")
        endpoint, data = mock_request.call_args[0]
        assert endpoint == "openOrder"

    def test_passes_amount_and_currency(self, client, mock_request):
        client.orders.open_order(amount="50.00", currency="EUR")
        _, data = mock_request.call_args[0]
        assert data["amount"] == "50.00"
        assert data["currency"] == "EUR"

    def test_includes_checksum(self, client, mock_request):
        client.orders.open_order(amount="10.00", currency="USD")
        _, data = mock_request.call_args[0]
        assert "checksum" in data

    def test_passes_optional_kwargs(self, client, mock_request):
        client.orders.open_order(
            amount="10.00", currency="USD",
            userTokenId="user_123", clientUniqueId="cu_1",
        )
        _, data = mock_request.call_args[0]
        assert data["userTokenId"] == "user_123"
        assert data["clientUniqueId"] == "cu_1"


class TestUpdateOrder:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.orders.update_order(
            sessionToken="tok", amount="20.00", currency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "updateOrder"

    def test_includes_session_token(self, client, mock_request):
        client.orders.update_order(
            sessionToken="tok_x", amount="20.00", currency="USD",
        )
        _, data = mock_request.call_args[0]
        assert data["sessionToken"] == "tok_x"


class TestGetOrderDetails:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.orders.get_order_details(sessionToken="tok_y")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getOrderDetails"


class TestOrderChecksumFields:
    def test_order_checksum_fields(self):
        assert ORDER_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "amount", "currency", "timeStamp", "secretKey",
        ]

    def test_order_details_checksum_fields(self):
        assert ORDER_DETAILS_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

    def test_open_order_shortcut(self, client, mock_request):
        """client.open_order() should delegate to orders.open_order()."""
        client.open_order(amount="1.00", currency="GBP")
        endpoint, data = mock_request.call_args[0]
        assert endpoint == "openOrder"
        assert data["amount"] == "1.00"

"""Tests for the Card Operations service."""

from __future__ import annotations

from nuvei.services.card_operations import CARD_TOKENIZATION_CHECKSUM_FIELDS


class TestCardTokenization:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.card_operations.card_tokenization(
            sessionToken="tok",
            cardData={
                "cardNumber": "4111111111111111",
                "cardHolderName": "John Doe",
                "expirationMonth": "12",
                "expirationYear": "2028",
                "CVV": "217",
            },
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "cardTokenization"

    def test_no_checksum(self, client, mock_request):
        """cardTokenization does not compute a checksum."""
        client.card_operations.card_tokenization(sessionToken="tok", cardData={})
        _, data = mock_request.call_args[0]
        assert "checksum" not in data

    def test_no_credential_injection(self, client, mock_request):
        """cardTokenization sends raw data without injecting merchant credentials."""
        client.card_operations.card_tokenization(sessionToken="tok", cardData={})
        _, data = mock_request.call_args[0]
        assert "merchantId" not in data


class TestGetCardDetails:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.card_operations.get_card_details(
            sessionToken="tok", cardNumber="411111",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getCardDetails"

    def test_injects_credentials(self, client, mock_request):
        client.card_operations.get_card_details(
            sessionToken="tok", cardNumber="411111",
        )
        _, data = mock_request.call_args[0]
        assert data["merchantId"] == "test_mid"
        assert "checksum" not in data


class TestCardOperationsChecksumFields:
    def test_tokenization_checksum_fields(self):
        assert CARD_TOKENIZATION_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

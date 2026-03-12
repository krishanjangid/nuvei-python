"""Integration tests verifying checksum computation for each endpoint.

These tests call each service method with known values and verify that
the resulting checksum matches the expected SHA-256 hash computed manually.
"""

from __future__ import annotations

import hashlib
from typing import Any

import pytest

from nuvei import Nuvei


@pytest.fixture
def client():
    c = Nuvei(
        merchant_id="mid_001",
        merchant_site_id="site_001",
        merchant_secret_key="secret_abc",
        environment="test",
    )
    yield c
    c.close()


def _sha256(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _capture_data(client) -> dict[str, Any]:
    """Replace client.request with a mock and return the captured data dict."""
    captured: dict[str, Any] = {}

    def fake_request(endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        captured.update(data)
        captured["_endpoint"] = endpoint
        return {"status": "SUCCESS", "errCode": 0, "sessionToken": "tok"}

    client.request = fake_request  # type: ignore[assignment]
    return captured


class TestGetSessionTokenChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.get_session_token(
            clientRequestId="req_1", timeStamp="20260101120000",
        )
        raw = "mid_001" + "site_001" + "req_1" + "20260101120000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestOpenOrderChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.orders.open_order(
            clientRequestId="req_2", amount="100.00", currency="USD",
            timeStamp="20260101130000",
        )
        raw = "mid_001" + "site_001" + "req_2" + "100.00" + "USD" + "20260101130000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestPaymentChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.payments.payment(
            clientRequestId="req_3", amount="50.00", currency="EUR",
            timeStamp="20260102100000", sessionToken="tok",
            paymentOption={"card": {}},
        )
        raw = "mid_001" + "site_001" + "req_3" + "50.00" + "EUR" + "20260102100000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestInitPaymentChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.payments.init_payment(
            clientRequestId="req_4", amount="25.00", currency="GBP",
            timeStamp="20260103110000", sessionToken="tok",
            paymentOption={"card": {}},
        )
        raw = "mid_001" + "site_001" + "req_4" + "25.00" + "GBP" + "20260103110000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestSettleTransactionChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.financial.settle_transaction(
            clientRequestId="req_5", clientUniqueId="cu_5",
            amount="50.00", currency="USD",
            relatedTransactionId="txn_orig",
            authCode="auth_01",
            descriptorMerchantName="TestCo",
            descriptorMerchantPhone="555-0100",
            comment="Settle test",
            urlDetails={"notificationUrl": "https://example.com/notify"},
            timeStamp="20260104120000",
        )
        raw = (
            "mid_001" + "site_001" + "req_5" + "cu_5"
            + "50.00" + "USD" + "txn_orig" + "auth_01"
            + "TestCo" + "555-0100" + "Settle test"
            + "https://example.com/notify"
            + "20260104120000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)

    def test_missing_optional_fields(self, client):
        """Optional fields missing from the request should be empty strings in checksum."""
        captured = _capture_data(client)
        client.financial.settle_transaction(
            clientRequestId="req_6",
            amount="30.00", currency="USD",
            relatedTransactionId="txn_orig2",
            authCode="auth_02",
            timeStamp="20260104130000",
        )
        raw = (
            "mid_001" + "site_001" + "req_6"
            + ""  # clientUniqueId missing
            + "30.00" + "USD" + "txn_orig2" + "auth_02"
            + ""  # descriptorMerchantName
            + ""  # descriptorMerchantPhone
            + ""  # comment
            + ""  # urlDetails
            + "20260104130000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestRefundTransactionChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.financial.refund_transaction(
            clientRequestId="req_7", clientUniqueId="cu_7",
            amount="10.00", currency="USD",
            relatedTransactionId="txn_orig3",
            authCode="auth_03",
            comment="Refund test",
            timeStamp="20260105100000",
        )
        raw = (
            "mid_001" + "site_001" + "req_7" + "cu_7"
            + "10.00" + "USD" + "txn_orig3" + "auth_03"
            + "Refund test"
            + ""  # urlDetails
            + "20260105100000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestPayoutChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.financial.payout(
            clientRequestId="req_8", amount="25.00", currency="USD",
            timeStamp="20260106100000",
            userTokenId="u1",
        )
        raw = "mid_001" + "site_001" + "req_8" + "25.00" + "USD" + "20260106100000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestAuthorize3dChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.three_d_secure.authorize3d(
            clientRequestId="req_9", amount="15.00", currency="USD",
            timeStamp="20260107100000", sessionToken="tok",
            paymentOption={"card": {"threeD": {}}},
        )
        raw = "mid_001" + "site_001" + "req_9" + "15.00" + "USD" + "20260107100000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestCreateUserChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.users.create_user(
            clientRequestId="req_10",
            userTokenId="u_tok_1",
            firstName="John", lastName="Doe",
            address="123 Main", state="NY", city="NYC",
            zip="10001", countryCode="US", phone="555-1234",
            locale="en_US", email="john@test.com", county="Manhattan",
            timeStamp="20260108100000",
        )
        raw = (
            "mid_001" + "site_001" + "u_tok_1" + "req_10"
            + "John" + "Doe" + "123 Main" + "NY" + "NYC" + "10001"
            + "US" + "555-1234" + "en_US" + "john@test.com" + "Manhattan"
            + "20260108100000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestAddUPOCreditCardChecksum:
    def test_checksum_with_billing_address(self, client):
        captured = _capture_data(client)
        client.user_payment_options.add_upo_credit_card(
            clientRequestId="req_11",
            userTokenId="u1",
            ccCardNumber="4111111111111111",
            ccExpMonth="12", ccExpYear="2028",
            ccNameOnCard="John Doe",
            billingAddress={
                "firstName": "John", "lastName": "Doe",
                "address": "123 Main", "phone": "555-0100",
                "zip": "10001", "city": "NYC",
                "countryCode": "US", "state": "NY",
                "email": "john@test.com", "county": "",
            },
            timeStamp="20260109100000",
        )
        ba = "JohnDoe123 Main555-010010001NYCUSNYjohn@test.com"
        raw = (
            "mid_001" + "site_001" + "u1" + "req_11"
            + "4111111111111111" + "12" + "2028" + "John Doe"
            + ba + "20260109100000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestCreateSubscriptionChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.subscriptions.create_subscription(
            clientRequestId="req_12",
            userTokenId="u1", planId="plan_1",
            userPaymentOptionId="upo_1",
            initialAmount="0.00", recurringAmount="9.99",
            currency="USD",
            timeStamp="20260110100000",
        )
        raw = (
            "mid_001" + "site_001" + "u1" + "plan_1"
            + "upo_1" + "0.00" + "9.99" + "USD"
            + "20260110100000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestCancelSubscriptionChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.subscriptions.cancel_subscription(
            subscriptionId="sub_1",
            timeStamp="20260111100000",
        )
        raw = "mid_001" + "site_001" + "sub_1" + "20260111100000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestCreatePlanChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.subscriptions.create_plan(
            name="Monthly", initialAmount="0", recurringAmount="9.99",
            currency="USD", timeStamp="20260112100000",
        )
        raw = (
            "mid_001" + "site_001" + "Monthly" + "0"
            + "9.99" + "USD" + "20260112100000" + "secret_abc"
        )
        assert captured["checksum"] == _sha256(raw)


class TestGetMerchantPaymentMethodsChecksum:
    def test_checksum_matches(self, client):
        captured = _capture_data(client)
        client.user_payment_options.get_merchant_payment_methods(
            clientRequestId="req_13",
            timeStamp="20260113100000",
        )
        raw = "mid_001" + "site_001" + "req_13" + "20260113100000" + "secret_abc"
        assert captured["checksum"] == _sha256(raw)


class TestMD5Algorithm:
    def test_md5_checksum(self):
        client = Nuvei(
            merchant_id="mid_001",
            merchant_site_id="site_001",
            merchant_secret_key="secret_abc",
            environment="test",
            algorithm="md5",
        )
        captured = _capture_data(client)
        client.get_session_token(
            clientRequestId="req_md5", timeStamp="20260101120000",
        )
        raw = "mid_001" + "site_001" + "req_md5" + "20260101120000" + "secret_abc"
        expected = hashlib.md5(raw.encode("utf-8")).hexdigest()
        assert captured["checksum"] == expected
        assert len(captured["checksum"]) == 32  # MD5 is 32 hex chars
        client.close()

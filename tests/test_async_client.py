"""Tests for the AsyncNuvei client."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from nuvei import AsyncNuvei


@pytest.fixture
def async_client():
    return AsyncNuvei(
        merchant_id="test_mid",
        merchant_site_id="123456",
        merchant_secret_key="test_secret_key",
        environment="test",
    )


@pytest.fixture
def mock_async_request(async_client, monkeypatch):
    response = {
        "status": "SUCCESS", "errCode": 0, "reason": "",
        "sessionToken": "async_tok_123",
    }
    mock = AsyncMock(return_value=response)
    monkeypatch.setattr(async_client, "request", mock)
    return mock


class TestAsyncClientInit:
    def test_attributes(self, async_client):
        assert async_client.merchant_id == "test_mid"
        assert async_client.merchant_site_id == "123456"
        assert async_client.algorithm == "sha256"

    def test_service_accessors(self, async_client):
        assert async_client.authentication is not None
        assert async_client.payments is not None
        assert async_client.financial is not None
        assert async_client.three_d_secure is not None
        assert async_client.card_operations is not None
        assert async_client.users is not None
        assert async_client.user_payment_options is not None
        assert async_client.subscriptions is not None
        assert async_client.orders is not None
        assert async_client.advanced_apm is not None


class TestAsyncGetSessionToken:
    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, async_client, mock_async_request):
        await async_client.get_session_token()
        mock_async_request.assert_awaited_once()
        endpoint, data = mock_async_request.call_args[0]
        assert endpoint == "getSessionToken"

    @pytest.mark.asyncio
    async def test_caches_session_token(self, async_client, mock_async_request):
        assert async_client.session_token is None
        await async_client.get_session_token()
        assert async_client.session_token == "async_tok_123"


class TestAsyncOpenOrder:
    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, async_client, mock_async_request):
        await async_client.open_order(amount="10.00", currency="USD")
        endpoint, _ = mock_async_request.call_args[0]
        assert endpoint == "openOrder"


class TestAsyncPayment:
    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, async_client, mock_async_request):
        await async_client.payments.payment(
            sessionToken="tok", amount="10.00", currency="USD",
            paymentOption={"card": {}},
        )
        endpoint, _ = mock_async_request.call_args[0]
        assert endpoint == "payment"


class TestAsyncFinancial:
    @pytest.mark.asyncio
    async def test_settle_transaction(self, async_client, mock_async_request):
        await async_client.financial.settle_transaction(
            relatedTransactionId="txn_1", amount="10.00",
            currency="USD", authCode="auth",
        )
        endpoint, _ = mock_async_request.call_args[0]
        assert endpoint == "settleTransaction"

    @pytest.mark.asyncio
    async def test_refund_transaction(self, async_client, mock_async_request):
        await async_client.financial.refund_transaction(
            relatedTransactionId="txn_1", amount="5.00",
            currency="USD", clientUniqueId="cu",
        )
        endpoint, _ = mock_async_request.call_args[0]
        assert endpoint == "refundTransaction"

    @pytest.mark.asyncio
    async def test_void_transaction(self, async_client, mock_async_request):
        await async_client.financial.void_transaction(
            relatedTransactionId="txn_1", amount="5.00", currency="USD",
        )
        endpoint, _ = mock_async_request.call_args[0]
        assert endpoint == "voidTransaction"


class TestAsyncContextManager:
    @pytest.mark.asyncio
    async def test_async_with(self):
        async with AsyncNuvei(
            merchant_id="m",
            merchant_site_id="s",
            merchant_secret_key="k",
            environment="test",
        ) as client:
            assert client.merchant_id == "m"

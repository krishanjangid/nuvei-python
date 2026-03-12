"""Financial operations — ``/settleTransaction``, ``/refundTransaction``,
``/voidTransaction``, ``/payout``, ``/getPayoutStatus``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

SETTLE_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
    "amount", "currency", "relatedTransactionId", "authCode",
    "descriptorMerchantName", "descriptorMerchantPhone", "comment",
    "urlDetails", "timeStamp", "secretKey",
]

REFUND_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
    "amount", "currency", "relatedTransactionId", "authCode",
    "comment", "urlDetails", "timeStamp", "secretKey",
]

VOID_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "clientUniqueId",
    "amount", "currency", "relatedTransactionId", "authCode",
    "comment", "urlDetails", "timeStamp", "secretKey",
]

PAYOUT_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "amount", "currency", "timeStamp", "secretKey",
]

PAYOUT_STATUS_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "timeStamp", "secretKey",
]


class FinancialService:
    """Synchronous financial operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def settle_transaction(self, **kwargs: Any) -> dict[str, Any]:
        """Settle a previously authorized transaction (``/settleTransaction``).

        Supports full and partial settlements. For partial settlements, call
        multiple times with different ``amount`` values.

        Required kwargs:
            relatedTransactionId, amount, currency, authCode
        Optional:
            clientUniqueId, descriptorMerchantName, descriptorMerchantPhone,
            comment, urlDetails
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, SETTLE_CHECKSUM_FIELDS)
        return self._client.request("settleTransaction", data)

    def refund_transaction(self, **kwargs: Any) -> dict[str, Any]:
        """Refund a previously settled transaction (``/refundTransaction``).

        The sum of all partial refunds must not exceed the original sale amount.

        Required kwargs:
            relatedTransactionId, amount, currency, clientUniqueId
        Optional:
            authCode, comment, urlDetails
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, REFUND_CHECKSUM_FIELDS)
        return self._client.request("refundTransaction", data)

    def void_transaction(self, **kwargs: Any) -> dict[str, Any]:
        """Void a transaction before it is settled (``/voidTransaction``).

        Must be called during the window between submission and transmission
        to the processor.

        Required kwargs:
            relatedTransactionId, amount, currency
        Optional:
            authCode, comment, urlDetails, clientUniqueId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, VOID_CHECKSUM_FIELDS)
        return self._client.request("voidTransaction", data)

    def payout(self, **kwargs: Any) -> dict[str, Any]:
        """Initiate a payout / credit to a payment method (``/payout``).

        Required kwargs:
            userTokenId, amount, currency, paymentOption or userPaymentOption
        Optional:
            clientUniqueId, comment, urlDetails, deviceDetails, userDetails,
            dynamicDescriptor
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYOUT_CHECKSUM_FIELDS)
        return self._client.request("payout", data)

    def get_payout_status(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve the status of a payout (``/getPayoutStatus``).

        Required kwargs:
            clientRequestId (the original payout's clientRequestId)
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYOUT_STATUS_CHECKSUM_FIELDS)
        return self._client.request("getPayoutStatus", data)


class AsyncFinancialService:
    """Asynchronous financial operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def settle_transaction(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, SETTLE_CHECKSUM_FIELDS)
        return await self._client.request("settleTransaction", data)

    async def refund_transaction(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, REFUND_CHECKSUM_FIELDS)
        return await self._client.request("refundTransaction", data)

    async def void_transaction(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, VOID_CHECKSUM_FIELDS)
        return await self._client.request("voidTransaction", data)

    async def payout(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYOUT_CHECKSUM_FIELDS)
        return await self._client.request("payout", data)

    async def get_payout_status(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYOUT_STATUS_CHECKSUM_FIELDS)
        return await self._client.request("getPayoutStatus", data)

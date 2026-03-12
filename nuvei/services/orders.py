"""Order management — ``/openOrder``, ``/updateOrder``, ``/getOrderDetails``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

ORDER_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "amount", "currency", "timeStamp", "secretKey",
]

ORDER_DETAILS_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "timeStamp", "secretKey",
]


class OrderService:
    """Synchronous order operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def open_order(self, **kwargs: Any) -> dict[str, Any]:
        """Open a new order session (``/openOrder``).

        Creates an authenticated order context and returns a ``sessionToken``
        that must be used for subsequent payment calls.

        Required kwargs:
            amount, currency
        Optional:
            userTokenId, clientUniqueId, dynamicDescriptor, merchantDetails,
            amountDetails, items, deviceDetails, userDetails,
            shippingAddress, billingAddress, addendums, urlDetails
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_CHECKSUM_FIELDS)
        return self._client.request("openOrder", data)

    def update_order(self, **kwargs: Any) -> dict[str, Any]:
        """Update an existing open order (``/updateOrder``).

        Required kwargs:
            sessionToken, amount, currency
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_CHECKSUM_FIELDS)
        return self._client.request("updateOrder", data)

    def get_order_details(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve details for an order (``/getOrderDetails``).

        Required kwargs:
            sessionToken or orderId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_DETAILS_CHECKSUM_FIELDS)
        return self._client.request("getOrderDetails", data)


class AsyncOrderService:
    """Asynchronous order operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def open_order(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_CHECKSUM_FIELDS)
        return await self._client.request("openOrder", data)

    async def update_order(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_CHECKSUM_FIELDS)
        return await self._client.request("updateOrder", data)

    async def get_order_details(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ORDER_DETAILS_CHECKSUM_FIELDS)
        return await self._client.request("getOrderDetails", data)

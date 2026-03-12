"""Payment services — ``/payment``, ``/paymentCC``, ``/paymentAPM``, ``/initPayment``,
``/accountCapture``, ``/getMcpRates``, ``/getDccDetails``, ``/getPaymentStatus``, ``/getCardDetails``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

PAYMENT_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "amount", "currency", "timeStamp", "secretKey",
]


class PaymentService:
    """Synchronous payment operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def payment(self, **kwargs: Any) -> dict[str, Any]:
        """Process a payment request (``/payment``).

        Supports ``transactionType`` values: ``"Sale"``, ``"Auth"``, ``"PreAuth"``.

        Required kwargs:
            sessionToken, amount, currency, paymentOption
        Optional:
            userTokenId, clientUniqueId, isRebilling, deviceDetails,
            billingAddress, shippingAddress, userDetails, merchantDetails,
            urlDetails, dynamicDescriptor, addendums, etc.
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return self._client.request("payment", data)

    def payment_cc(self, **kwargs: Any) -> dict[str, Any]:
        """Process a credit-card payment (``/paymentCC``, legacy endpoint)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return self._client.request("paymentCC", data)

    def payment_apm(self, **kwargs: Any) -> dict[str, Any]:
        """Process an Alternative Payment Method payment (``/paymentAPM``).

        Additional required kwargs:
            paymentMethod
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return self._client.request("paymentAPM", data)

    def init_payment(self, **kwargs: Any) -> dict[str, Any]:
        """Initialize a payment — determines 3DS support (``/initPayment``).

        This call must precede ``/payment`` when 3D Secure is required.

        Required kwargs:
            sessionToken, amount, currency, paymentOption
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return self._client.request("initPayment", data)

    def get_payment_status(self, session_token: str) -> dict[str, Any]:
        """Retrieve the status of the most recent payment for a session (``/getPaymentStatus``).

        Args:
            session_token: The session token from ``openOrder`` or ``getSessionToken``.
        """
        data: dict[str, Any] = {"sessionToken": session_token}
        data = self._client._inject_credentials(data)
        return self._client.request("getPaymentStatus", data)

    def account_capture(self, **kwargs: Any) -> dict[str, Any]:
        """Capture APM account details for future use (``/accountCapture``).

        Required kwargs:
            sessionToken, userTokenId, paymentMethod, currencyCode,
            countryCode, amount
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("accountCapture", data)

    def get_mcp_rates(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve Multi-Currency Pricing (MCP) exchange rates (``/getMcpRates``).

        Required kwargs:
            sessionToken, fromCurrency
        Optional:
            toCurrency, paymentOption
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("getMcpRates", data)

    def get_dcc_details(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve Dynamic Currency Conversion details (``/getDccDetails``).

        Required kwargs:
            sessionToken, clientUniqueId, originalAmount, originalCurrency
        Optional:
            paymentOption, cardNumber
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("getDccDetails", data)


class AsyncPaymentService:
    """Asynchronous payment operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def payment(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return await self._client.request("payment", data)

    async def payment_cc(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return await self._client.request("paymentCC", data)

    async def payment_apm(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return await self._client.request("paymentAPM", data)

    async def init_payment(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, PAYMENT_CHECKSUM_FIELDS)
        return await self._client.request("initPayment", data)

    async def get_payment_status(self, session_token: str) -> dict[str, Any]:
        data: dict[str, Any] = {"sessionToken": session_token}
        data = self._client._inject_credentials(data)
        return await self._client.request("getPaymentStatus", data)

    async def account_capture(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("accountCapture", data)

    async def get_mcp_rates(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("getMcpRates", data)

    async def get_dcc_details(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("getDccDetails", data)

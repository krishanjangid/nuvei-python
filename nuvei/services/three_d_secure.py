"""3D Secure services — ``/authorize3d``, ``/verify3d``, ``/dynamic3D``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

AUTHORIZE3D_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "amount", "currency", "timeStamp", "secretKey",
]

DYNAMIC3D_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "amount", "currency", "timeStamp", "secretKey",
]


class ThreeDSecureService:
    """Synchronous 3D Secure operations.

    Typical 3DS 2.0 flow:
        1. ``initPayment`` → check if card supports 3DS, get ``threeD`` data
        2. Perform 3DS fingerprinting (client-side iframe)
        3. ``authorize3d`` → submit 3DS challenge result
        4. ``verify3d`` → verify the 3DS authentication
        5. ``payment`` → complete the payment with liability shift

    For 3DS Method (fingerprinting), pass
    ``paymentOption.card.threeD.methodNotificationUrl`` in the ``initPayment`` call.
    """

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def authorize3d(self, **kwargs: Any) -> dict[str, Any]:
        """Submit 3D Secure authorization (``/authorize3d``).

        Called after the cardholder completes the 3DS challenge. Sends the
        authentication data to Nuvei for verification.

        Required kwargs:
            sessionToken, amount, currency, paymentOption, relatedTransactionId
        The ``paymentOption.card.threeD`` object should contain the 3DS result
        fields from the challenge.
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, AUTHORIZE3D_CHECKSUM_FIELDS)
        return self._client.request("authorize3d", data)

    def verify3d(self, **kwargs: Any) -> dict[str, Any]:
        """Verify 3D Secure authentication result (``/verify3d``).

        Required kwargs:
            sessionToken, amount, currency, paymentOption
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("verify3d", data)

    def dynamic3d(self, **kwargs: Any) -> dict[str, Any]:
        """Legacy Dynamic 3D endpoint (``/dynamic3D``).

        Required kwargs:
            sessionToken, amount, currency, paymentOption
        Optional:
            isDynamic3D, dynamic3DMode
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, DYNAMIC3D_CHECKSUM_FIELDS)
        return self._client.request("dynamic3D", data)


class AsyncThreeDSecureService:
    """Asynchronous 3D Secure operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def authorize3d(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, AUTHORIZE3D_CHECKSUM_FIELDS)
        return await self._client.request("authorize3d", data)

    async def verify3d(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("verify3d", data)

    async def dynamic3d(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, DYNAMIC3D_CHECKSUM_FIELDS)
        return await self._client.request("dynamic3D", data)

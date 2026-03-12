"""Card operations — ``/cardTokenization``, ``/getCardDetails``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

CARD_TOKENIZATION_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "timeStamp", "secretKey",
]


class CardOperationsService:
    """Synchronous card operation endpoints."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def card_tokenization(self, **kwargs: Any) -> dict[str, Any]:
        """Tokenize a credit card (``/cardTokenization``).

        Stores card details and returns a temporary token that can be used
        in subsequent payment requests.

        Required kwargs:
            sessionToken, cardData (object with cardNumber, cardHolderName,
            expirationMonth, expirationYear, CVV)
        """
        data: dict[str, Any] = {**kwargs}
        return self._client.request("cardTokenization", data)

    def get_card_details(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve card details by BIN (``/getCardDetails``).

        Returns card brand, type (credit/debit), issuing country, and whether
        the card supports 3D Secure. Useful for co-badged card detection.

        Required kwargs:
            sessionToken, cardNumber (first 6-8 digits, i.e. BIN)
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("getCardDetails", data)


class AsyncCardOperationsService:
    """Asynchronous card operation endpoints."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def card_tokenization(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        return await self._client.request("cardTokenization", data)

    async def get_card_details(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("getCardDetails", data)

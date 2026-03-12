"""Advanced APM Integration service.

Endpoints: ``/addBankAccount``, ``/enrollAccount``, ``/fundAccount``,
``/getAccountDetails``, ``/getDocumentUrl``.

These endpoints provide advanced APM operations for bank account management,
enrollment, and funding.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei


class AdvancedAPMService:
    """Synchronous advanced APM integration operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def add_bank_account(self, **kwargs: Any) -> dict[str, Any]:
        """Add a bank account for an APM (``/addBankAccount``).

        Required kwargs:
            sessionToken, paymentOption.alternativePaymentMethod.paymentMethod,
            userId, bankAccount.accountNumber, bankAccount.routingNumber,
            userTokenId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("addBankAccount", data)

    def enroll_account(self, **kwargs: Any) -> dict[str, Any]:
        """Enroll a user account for an APM (``/enrollAccount``).

        Required kwargs:
            sessionToken, clientUniqueId,
            paymentOption.alternativePaymentMethod.paymentMethod,
            userId, userTokenId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("enrollAccount", data)

    def fund_account(self, **kwargs: Any) -> dict[str, Any]:
        """Fund a user account via APM (``/fundAccount``).

        Required kwargs:
            sessionToken, clientUniqueId,
            paymentOption.alternativePaymentMethod.paymentMethod,
            userId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("fundAccount", data)

    def get_account_details(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve APM account details (``/getAccountDetails``).

        Required kwargs:
            sessionToken, clientUniqueId,
            paymentOption.alternativePaymentMethod.paymentMethod,
            userId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("getAccountDetails", data)

    def get_document_url(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve the URL for a specific APM document (``/getDocumentUrl``).

        Required kwargs:
            sessionToken, clientUniqueId,
            paymentOption.alternativePaymentMethod.paymentMethod,
            documentType
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return self._client.request("getDocumentUrl", data)


class AsyncAdvancedAPMService:
    """Asynchronous advanced APM integration operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def add_bank_account(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("addBankAccount", data)

    async def enroll_account(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("enrollAccount", data)

    async def fund_account(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("fundAccount", data)

    async def get_account_details(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("getAccountDetails", data)

    async def get_document_url(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._inject_credentials(data)
        return await self._client.request("getDocumentUrl", data)

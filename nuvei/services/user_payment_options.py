"""User Payment Option (UPO) management.

Endpoints: ``/addUPOCreditCard``, ``/addUPOCreditCardByTempToken``,
``/addUPOCreditCardByToken``, ``/getUserUPOs``, ``/editUPOCC``,
``/editUPOAPM``, ``/deleteUPO``, ``/suspendUPO``, ``/enableUPO``,
``/addUPOAPM``, ``/getMerchantPaymentMethods``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

UPO_SIMPLE_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "userPaymentOptionId", "timeStamp", "secretKey",
]

UPO_SESSION_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "timeStamp", "secretKey",
]

GET_UPOS_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "timeStamp", "secretKey",
]

ADD_CREDIT_CARD_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "ccCardNumber", "ccExpMonth", "ccExpYear", "ccNameOnCard",
    "billingAddress", "timeStamp", "secretKey",
]

ADD_CREDIT_CARD_BY_TOKEN_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "ccExpMonth", "ccExpYear", "ccNameOnCard", "ccToken",
    "brand", "uniqueCC", "bin", "last4Digits",
    "billingAddress", "timeStamp", "secretKey",
]

ADD_UPO_APM_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "paymentMethodName", "apmData", "billingAddress", "timeStamp", "secretKey",
]

EDIT_UPO_CC_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "userPaymentOptionId", "ccExpMonth", "ccExpYear", "ccNameOnCard",
    "billingAddress", "timeStamp", "secretKey",
]

EDIT_UPO_APM_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "userPaymentOptionId", "apmData", "billingAddress", "timeStamp", "secretKey",
]

MERCHANT_PM_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "timeStamp", "secretKey",
]


class UserPaymentOptionService:
    """Synchronous UPO management."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def add_upo_credit_card(self, **kwargs: Any) -> dict[str, Any]:
        """Add a credit card as a User Payment Option (``/addUPOCreditCard``).

        Required kwargs:
            userTokenId, ccCardNumber, ccExpMonth, ccExpYear, ccNameOnCard
        Optional:
            billingAddress (object), userPaymentOptionId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_CREDIT_CARD_CHECKSUM_FIELDS)
        return self._client.request("addUPOCreditCard", data)

    def add_upo_credit_card_by_temp_token(self, **kwargs: Any) -> dict[str, Any]:
        """Add a credit card UPO using a temporary token (``/addUPOCreditCardByTempToken``).

        Required kwargs:
            sessionToken, userTokenId, ccTempToken
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SESSION_CHECKSUM_FIELDS)
        return self._client.request("addUPOCreditCardByTempToken", data)

    def add_upo_credit_card_by_token(self, **kwargs: Any) -> dict[str, Any]:
        """Add a credit card UPO by permanent token (``/addUPOCreditCardByToken``).

        Required kwargs:
            userTokenId, ccExpMonth, ccExpYear, ccNameOnCard, ccToken,
            brand, uniqueCC, bin, last4Digits
        Optional:
            billingAddress
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_CREDIT_CARD_BY_TOKEN_CHECKSUM_FIELDS)
        return self._client.request("addUPOCreditCardByToken", data)

    def add_upo_apm(self, **kwargs: Any) -> dict[str, Any]:
        """Add an Alternative Payment Method as a UPO (``/addUPOAPM``).

        Required kwargs:
            userTokenId, paymentMethodName, apmData (object)
        Optional:
            billingAddress
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_UPO_APM_CHECKSUM_FIELDS)
        return self._client.request("addUPOAPM", data)

    def edit_upo_cc(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing credit card UPO (``/editUPOCC``).

        Required kwargs:
            userTokenId, userPaymentOptionId, ccExpMonth, ccExpYear, ccNameOnCard
        Optional:
            billingAddress
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_UPO_CC_CHECKSUM_FIELDS)
        return self._client.request("editUPOCC", data)

    def edit_upo_apm(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing APM UPO (``/editUPOAPM``).

        Required kwargs:
            userTokenId, userPaymentOptionId, apmData (object)
        Optional:
            billingAddress
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_UPO_APM_CHECKSUM_FIELDS)
        return self._client.request("editUPOAPM", data)

    def get_user_upos(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve all UPOs for a user (``/getUserUPOs``).

        Required kwargs:
            userTokenId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_UPOS_CHECKSUM_FIELDS)
        return self._client.request("getUserUPOs", data)

    def delete_upo(self, **kwargs: Any) -> dict[str, Any]:
        """Permanently delete a UPO (``/deleteUPO``).

        Required kwargs:
            userTokenId, userPaymentOptionId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return self._client.request("deleteUPO", data)

    def suspend_upo(self, **kwargs: Any) -> dict[str, Any]:
        """Temporarily suspend a UPO (``/suspendUPO``).

        Required kwargs:
            userTokenId, userPaymentOptionId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return self._client.request("suspendUPO", data)

    def enable_upo(self, **kwargs: Any) -> dict[str, Any]:
        """Re-enable a previously suspended UPO (``/enableUPO``).

        Required kwargs:
            userTokenId, userPaymentOptionId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return self._client.request("enableUPO", data)

    def get_merchant_payment_methods(self, **kwargs: Any) -> dict[str, Any]:
        """List all payment methods available for the merchant (``/getMerchantPaymentMethods``).

        Optional kwargs:
            sessionToken, currencyCode, countryCode, languageCode
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, MERCHANT_PM_CHECKSUM_FIELDS)
        return self._client.request("getMerchantPaymentMethods", data)


class AsyncUserPaymentOptionService:
    """Asynchronous UPO management."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def add_upo_credit_card(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_CREDIT_CARD_CHECKSUM_FIELDS)
        return await self._client.request("addUPOCreditCard", data)

    async def add_upo_credit_card_by_temp_token(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SESSION_CHECKSUM_FIELDS)
        return await self._client.request("addUPOCreditCardByTempToken", data)

    async def add_upo_credit_card_by_token(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_CREDIT_CARD_BY_TOKEN_CHECKSUM_FIELDS)
        return await self._client.request("addUPOCreditCardByToken", data)

    async def add_upo_apm(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, ADD_UPO_APM_CHECKSUM_FIELDS)
        return await self._client.request("addUPOAPM", data)

    async def edit_upo_cc(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_UPO_CC_CHECKSUM_FIELDS)
        return await self._client.request("editUPOCC", data)

    async def edit_upo_apm(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_UPO_APM_CHECKSUM_FIELDS)
        return await self._client.request("editUPOAPM", data)

    async def get_user_upos(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_UPOS_CHECKSUM_FIELDS)
        return await self._client.request("getUserUPOs", data)

    async def delete_upo(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return await self._client.request("deleteUPO", data)

    async def suspend_upo(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return await self._client.request("suspendUPO", data)

    async def enable_upo(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, UPO_SIMPLE_CHECKSUM_FIELDS)
        return await self._client.request("enableUPO", data)

    async def get_merchant_payment_methods(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, MERCHANT_PM_CHECKSUM_FIELDS)
        return await self._client.request("getMerchantPaymentMethods", data)

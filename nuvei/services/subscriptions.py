"""Subscription / rebilling management.

Plan endpoints: ``/createPlan``, ``/editPlan``, ``/getPlansList``.
Subscription endpoints: ``/createSubscription``, ``/editSubscription``,
``/cancelSubscription``, ``/getSubscriptionsList``.
Legacy: ``/getSubscriptionPlans``.

Nuvei subscriptions support two modes:
  - **Automatic**: Nuvei processes payments on schedule and notifies the merchant.
  - **Manual**: The merchant triggers each rebilling via API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

CREATE_PLAN_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "name", "initialAmount",
    "recurringAmount", "currency", "timeStamp", "secretKey",
]

EDIT_PLAN_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "planId", "initialAmount",
    "recurringAmount", "currency", "timeStamp", "secretKey",
]

GET_PLANS_LIST_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "planIds", "currency",
    "planStatus", "timeStamp", "secretKey",
]

CREATE_SUBSCRIPTION_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "planId",
    "userPaymentOptionId", "initialAmount", "recurringAmount",
    "currency", "timeStamp", "secretKey",
]

EDIT_SUBSCRIPTION_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "subscriptionId",
    "userPaymentOptionId", "recurringAmount", "currency",
    "timeStamp", "secretKey",
]

CANCEL_SUBSCRIPTION_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "subscriptionId",
    "timeStamp", "secretKey",
]

GET_SUBSCRIPTIONS_LIST_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "planIds",
    "subscriptionIds", "subscriptionStatus", "timeStamp", "secretKey",
]

GET_SUBSCRIPTION_PLANS_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId",
    "timeStamp", "secretKey",
]


class SubscriptionService:
    """Synchronous subscription/rebilling operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    # ---- Plan management ----

    def create_plan(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new rebilling plan (``/createPlan``).

        Required kwargs:
            name, recurringAmount, currency,
            endAfter (object with day/month/year)
        Optional:
            initialAmount, startAfter, planStatus
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CREATE_PLAN_CHECKSUM_FIELDS)
        return self._client.request("createPlan", data)

    def edit_plan(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing rebilling plan (``/editPlan``).

        Required kwargs:
            planId
        Optional:
            name, initialAmount, recurringAmount, currency,
            endAfter, startAfter, planStatus
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_PLAN_CHECKSUM_FIELDS)
        return self._client.request("editPlan", data)

    def get_plans_list(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a list of rebilling plans (``/getPlansList``).

        Optional kwargs:
            planIds, currency, planStatus
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_PLANS_LIST_CHECKSUM_FIELDS)
        return self._client.request("getPlansList", data)

    # ---- Subscription management ----

    def create_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new recurring subscription (``/createSubscription``).

        Required kwargs:
            userTokenId, planId, userPaymentOptionId, endAfter
        Optional:
            initialAmount, recurringAmount, currency,
            startAfter, dynamicDescriptor, deviceDetails,
            userDetails, billingAddress, urlDetails
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CREATE_SUBSCRIPTION_CHECKSUM_FIELDS)
        return self._client.request("createSubscription", data)

    def edit_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing subscription (``/editSubscription``).

        Required kwargs:
            subscriptionId
        Optional:
            userPaymentOptionId, recurringAmount, currency,
            endAfter, startAfter
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_SUBSCRIPTION_CHECKSUM_FIELDS)
        return self._client.request("editSubscription", data)

    def cancel_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Cancel an existing subscription (``/cancelSubscription``).

        Required kwargs:
            subscriptionId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CANCEL_SUBSCRIPTION_CHECKSUM_FIELDS)
        return self._client.request("cancelSubscription", data)

    def get_subscriptions_list(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a list of subscriptions (``/getSubscriptionsList``).

        Optional kwargs:
            userTokenId, planIds, subscriptionIds, subscriptionStatus
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_SUBSCRIPTIONS_LIST_CHECKSUM_FIELDS)
        return self._client.request("getSubscriptionsList", data)

    def get_subscription_plans(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve subscription plans — legacy endpoint (``/getSubscriptionPlans``).

        Prefer :meth:`get_plans_list` for new integrations.
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_SUBSCRIPTION_PLANS_CHECKSUM_FIELDS)
        return self._client.request("getSubscriptionPlans", data)


class AsyncSubscriptionService:
    """Asynchronous subscription/rebilling operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    # ---- Plan management ----

    async def create_plan(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new rebilling plan (``/createPlan``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CREATE_PLAN_CHECKSUM_FIELDS)
        return await self._client.request("createPlan", data)

    async def edit_plan(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing rebilling plan (``/editPlan``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_PLAN_CHECKSUM_FIELDS)
        return await self._client.request("editPlan", data)

    async def get_plans_list(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a list of rebilling plans (``/getPlansList``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_PLANS_LIST_CHECKSUM_FIELDS)
        return await self._client.request("getPlansList", data)

    # ---- Subscription management ----

    async def create_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new recurring subscription (``/createSubscription``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CREATE_SUBSCRIPTION_CHECKSUM_FIELDS)
        return await self._client.request("createSubscription", data)

    async def edit_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an existing subscription (``/editSubscription``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, EDIT_SUBSCRIPTION_CHECKSUM_FIELDS)
        return await self._client.request("editSubscription", data)

    async def cancel_subscription(self, **kwargs: Any) -> dict[str, Any]:
        """Cancel an existing subscription (``/cancelSubscription``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, CANCEL_SUBSCRIPTION_CHECKSUM_FIELDS)
        return await self._client.request("cancelSubscription", data)

    async def get_subscriptions_list(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a list of subscriptions (``/getSubscriptionsList``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_SUBSCRIPTIONS_LIST_CHECKSUM_FIELDS)
        return await self._client.request("getSubscriptionsList", data)

    async def get_subscription_plans(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve subscription plans — legacy endpoint (``/getSubscriptionPlans``)."""
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_SUBSCRIPTION_PLANS_CHECKSUM_FIELDS)
        return await self._client.request("getSubscriptionPlans", data)

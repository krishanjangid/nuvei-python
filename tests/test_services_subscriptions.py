"""Tests for the Subscriptions service."""

from __future__ import annotations

from nuvei.services.subscriptions import (
    CANCEL_SUBSCRIPTION_CHECKSUM_FIELDS,
    CREATE_PLAN_CHECKSUM_FIELDS,
    CREATE_SUBSCRIPTION_CHECKSUM_FIELDS,
    EDIT_PLAN_CHECKSUM_FIELDS,
    EDIT_SUBSCRIPTION_CHECKSUM_FIELDS,
    GET_PLANS_LIST_CHECKSUM_FIELDS,
    GET_SUBSCRIPTION_PLANS_CHECKSUM_FIELDS,
    GET_SUBSCRIPTIONS_LIST_CHECKSUM_FIELDS,
)


class TestCreatePlan:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.create_plan(
            name="Monthly Plan", recurringAmount="9.99", currency="USD",
            endAfter={"day": "0", "month": "12", "year": "0"},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "createPlan"

    def test_includes_checksum(self, client, mock_request):
        client.subscriptions.create_plan(
            name="Plan", recurringAmount="5.00", currency="USD",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestEditPlan:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.edit_plan(
            planId="plan_1", recurringAmount="14.99", currency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "editPlan"


class TestGetPlansList:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.get_plans_list()
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getPlansList"

    def test_passes_optional_filters(self, client, mock_request):
        client.subscriptions.get_plans_list(
            planIds="plan_1,plan_2", currency="USD", planStatus="ACTIVE",
        )
        _, data = mock_request.call_args[0]
        assert data["planIds"] == "plan_1,plan_2"
        assert data["planStatus"] == "ACTIVE"


class TestCreateSubscription:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.create_subscription(
            userTokenId="u1", planId="plan_1",
            userPaymentOptionId="upo_1",
            endAfter={"day": "0", "month": "0", "year": "1"},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "createSubscription"

    def test_includes_checksum(self, client, mock_request):
        client.subscriptions.create_subscription(
            userTokenId="u1", planId="plan_1",
            userPaymentOptionId="upo_1",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestEditSubscription:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.edit_subscription(
            subscriptionId="sub_1", recurringAmount="19.99", currency="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "editSubscription"


class TestCancelSubscription:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.cancel_subscription(subscriptionId="sub_1")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "cancelSubscription"

    def test_includes_checksum(self, client, mock_request):
        client.subscriptions.cancel_subscription(subscriptionId="sub_1")
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestGetSubscriptionsList:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.get_subscriptions_list(userTokenId="u1")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getSubscriptionsList"

    def test_passes_filters(self, client, mock_request):
        client.subscriptions.get_subscriptions_list(
            userTokenId="u1", subscriptionStatus="ACTIVE",
        )
        _, data = mock_request.call_args[0]
        assert data["subscriptionStatus"] == "ACTIVE"


class TestGetSubscriptionPlans:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.subscriptions.get_subscription_plans()
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getSubscriptionPlans"


class TestSubscriptionChecksumFields:
    def test_create_plan_checksum_fields(self):
        assert CREATE_PLAN_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "name", "initialAmount",
            "recurringAmount", "currency", "timeStamp", "secretKey",
        ]

    def test_edit_plan_checksum_fields(self):
        assert EDIT_PLAN_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "planId", "initialAmount",
            "recurringAmount", "currency", "timeStamp", "secretKey",
        ]

    def test_get_plans_list_checksum_fields(self):
        assert GET_PLANS_LIST_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "planIds", "currency",
            "planStatus", "timeStamp", "secretKey",
        ]

    def test_create_subscription_checksum_fields(self):
        assert CREATE_SUBSCRIPTION_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "planId",
            "userPaymentOptionId", "initialAmount", "recurringAmount",
            "currency", "timeStamp", "secretKey",
        ]

    def test_edit_subscription_checksum_fields(self):
        assert EDIT_SUBSCRIPTION_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "subscriptionId",
            "userPaymentOptionId", "recurringAmount", "currency",
            "timeStamp", "secretKey",
        ]

    def test_cancel_subscription_checksum_fields(self):
        assert CANCEL_SUBSCRIPTION_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "subscriptionId",
            "timeStamp", "secretKey",
        ]

    def test_get_subscriptions_list_checksum_fields(self):
        assert GET_SUBSCRIPTIONS_LIST_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "planIds",
            "subscriptionIds", "subscriptionStatus", "timeStamp", "secretKey",
        ]

    def test_get_subscription_plans_checksum_fields(self):
        assert GET_SUBSCRIPTION_PLANS_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

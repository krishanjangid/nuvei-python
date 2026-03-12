"""Tests for the User Payment Options service."""

from __future__ import annotations

from nuvei.services.user_payment_options import (
    ADD_CREDIT_CARD_BY_TOKEN_CHECKSUM_FIELDS,
    ADD_CREDIT_CARD_CHECKSUM_FIELDS,
    ADD_UPO_APM_CHECKSUM_FIELDS,
    EDIT_UPO_APM_CHECKSUM_FIELDS,
    EDIT_UPO_CC_CHECKSUM_FIELDS,
    GET_UPOS_CHECKSUM_FIELDS,
    MERCHANT_PM_CHECKSUM_FIELDS,
    UPO_SESSION_CHECKSUM_FIELDS,
    UPO_SIMPLE_CHECKSUM_FIELDS,
)


class TestAddUPOCreditCard:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.add_upo_credit_card(
            userTokenId="u1", ccCardNumber="4111111111111111",
            ccExpMonth="12", ccExpYear="2028", ccNameOnCard="John Doe",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "addUPOCreditCard"

    def test_includes_checksum(self, client, mock_request):
        client.user_payment_options.add_upo_credit_card(
            userTokenId="u1", ccCardNumber="4111111111111111",
            ccExpMonth="12", ccExpYear="2028", ccNameOnCard="John Doe",
        )
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestAddUPOCreditCardByTempToken:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.add_upo_credit_card_by_temp_token(
            sessionToken="tok", userTokenId="u1", ccTempToken="tmp_tok",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "addUPOCreditCardByTempToken"


class TestAddUPOCreditCardByToken:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.add_upo_credit_card_by_token(
            userTokenId="u1", ccExpMonth="12", ccExpYear="2028",
            ccNameOnCard="Jane", ccToken="cc_tok",
            brand="visa", uniqueCC="uniq", bin="411111", last4Digits="1111",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "addUPOCreditCardByToken"


class TestAddUPOAPM:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.add_upo_apm(
            userTokenId="u1", paymentMethodName="apmgw_Neteller",
            apmData={"account_id": "123"},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "addUPOAPM"


class TestEditUPOCC:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.edit_upo_cc(
            userTokenId="u1", userPaymentOptionId="upo_1",
            ccExpMonth="01", ccExpYear="2030", ccNameOnCard="Jane",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "editUPOCC"


class TestEditUPOAPM:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.edit_upo_apm(
            userTokenId="u1", userPaymentOptionId="upo_2",
            apmData={"account_id": "456"},
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "editUPOAPM"


class TestGetUserUPOs:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.get_user_upos(userTokenId="u1")
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getUserUPOs"

    def test_includes_checksum(self, client, mock_request):
        client.user_payment_options.get_user_upos(userTokenId="u1")
        _, data = mock_request.call_args[0]
        assert "checksum" in data


class TestDeleteUPO:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.delete_upo(
            userTokenId="u1", userPaymentOptionId="upo_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "deleteUPO"


class TestSuspendUPO:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.suspend_upo(
            userTokenId="u1", userPaymentOptionId="upo_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "suspendUPO"


class TestEnableUPO:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.enable_upo(
            userTokenId="u1", userPaymentOptionId="upo_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "enableUPO"


class TestGetMerchantPaymentMethods:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.user_payment_options.get_merchant_payment_methods(
            sessionToken="tok", currencyCode="USD",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getMerchantPaymentMethods"


class TestUPOChecksumFields:
    def test_simple_checksum_fields(self):
        assert UPO_SIMPLE_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "userPaymentOptionId", "timeStamp", "secretKey",
        ]

    def test_session_checksum_fields(self):
        assert UPO_SESSION_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

    def test_get_upos_checksum_fields(self):
        assert GET_UPOS_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

    def test_add_credit_card_checksum_fields(self):
        assert ADD_CREDIT_CARD_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "ccCardNumber", "ccExpMonth", "ccExpYear", "ccNameOnCard",
            "billingAddress", "timeStamp", "secretKey",
        ]

    def test_add_credit_card_by_token_checksum_fields(self):
        assert ADD_CREDIT_CARD_BY_TOKEN_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "ccExpMonth", "ccExpYear", "ccNameOnCard", "ccToken",
            "brand", "uniqueCC", "bin", "last4Digits",
            "billingAddress", "timeStamp", "secretKey",
        ]

    def test_add_upo_apm_checksum_fields(self):
        assert ADD_UPO_APM_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "paymentMethodName", "apmData", "billingAddress",
            "timeStamp", "secretKey",
        ]

    def test_edit_upo_cc_checksum_fields(self):
        assert EDIT_UPO_CC_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "userPaymentOptionId", "ccExpMonth", "ccExpYear", "ccNameOnCard",
            "billingAddress", "timeStamp", "secretKey",
        ]

    def test_edit_upo_apm_checksum_fields(self):
        assert EDIT_UPO_APM_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
            "userPaymentOptionId", "apmData", "billingAddress",
            "timeStamp", "secretKey",
        ]

    def test_merchant_pm_checksum_fields(self):
        assert MERCHANT_PM_CHECKSUM_FIELDS == [
            "merchantId", "merchantSiteId", "clientRequestId",
            "timeStamp", "secretKey",
        ]

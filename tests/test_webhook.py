"""Tests for webhook/DMN verification."""

import hashlib

import pytest

from nuvei.exceptions import ChecksumError
from nuvei.webhook import verify_webhook, verify_webhook_generic


class TestVerifyWebhook:
    def _make_params(self, secret: str, algorithm: str = "sha256") -> dict:
        params = {
            "totalAmount": "10.00",
            "currency": "USD",
            "responseTimeStamp": "2026-03-12.12:00:00",
            "PPP_TransactionID": "123456",
            "Status": "APPROVED",
            "productId": "prod_1",
        }
        raw = secret + "10.00USD2026-03-12.12:00:00123456APPROVEDprod_1"
        params["advanceResponseChecksum"] = hashlib.new(algorithm, raw.encode()).hexdigest()
        return params

    def test_valid_webhook(self):
        params = self._make_params("mysecret")
        assert verify_webhook(params, "mysecret") is True

    def test_invalid_webhook_raises(self):
        params = self._make_params("mysecret")
        with pytest.raises(ChecksumError):
            verify_webhook(params, "wrongsecret")

    def test_invalid_webhook_no_raise(self):
        params = self._make_params("mysecret")
        assert verify_webhook(params, "wrongsecret", raise_on_failure=False) is False

    def test_missing_checksum_raises(self):
        with pytest.raises(ChecksumError, match="No advanceResponseChecksum"):
            verify_webhook({}, "secret")

    def test_md5_algorithm(self):
        params = self._make_params("sec", algorithm="md5")
        assert verify_webhook(params, "sec", algorithm="md5") is True


class TestVerifyWebhookGeneric:
    def test_custom_fields(self):
        secret = "key123"
        params = {"fieldA": "val1", "fieldB": "val2"}
        raw = secret + "val1val2"
        params["myChecksum"] = hashlib.sha256(raw.encode()).hexdigest()

        assert verify_webhook_generic(
            params,
            secret,
            ["fieldA", "fieldB"],
            checksum_param="myChecksum",
        ) is True

    def test_suffix_secret(self):
        secret = "key"
        params = {"a": "1", "b": "2"}
        raw = "12" + secret
        params["cs"] = hashlib.sha256(raw.encode()).hexdigest()

        assert verify_webhook_generic(
            params, secret, ["a", "b"],
            checksum_param="cs",
            secret_position="suffix",
        ) is True

"""Tests for checksum calculation."""

import hashlib

from nuvei.checksum import build_checksum_string, calculate_checksum


class TestCalculateChecksum:
    def test_sha256_basic(self):
        result = calculate_checksum(["hello", "world"], algorithm="sha256")
        expected = hashlib.sha256(b"helloworld").hexdigest()
        assert result == expected

    def test_md5_basic(self):
        result = calculate_checksum(["foo", "bar"], algorithm="md5")
        expected = hashlib.md5(b"foobar").hexdigest()
        assert result == expected

    def test_empty_values(self):
        result = calculate_checksum(["", "", ""], algorithm="sha256")
        expected = hashlib.sha256(b"").hexdigest()
        assert result == expected


class TestBuildChecksumString:
    def test_simple_fields(self):
        data = {"merchantId": "123", "merchantSiteId": "456", "timeStamp": "20260101120000"}
        fields = ["merchantId", "merchantSiteId", "timeStamp", "secretKey"]
        result = build_checksum_string(data, fields, merchant_secret_key="secret")
        assert result == "12345620260101120000secret"

    def test_missing_fields_default_empty(self):
        data = {"merchantId": "123"}
        fields = ["merchantId", "merchantSiteId", "secretKey"]
        result = build_checksum_string(data, fields, merchant_secret_key="key")
        assert result == "123key"

    def test_self_data_fallback(self):
        data = {"timeStamp": "20260101120000"}
        fields = ["merchantId", "timeStamp", "secretKey"]
        result = build_checksum_string(
            data,
            fields,
            merchant_secret_key="sec",
            self_data={"merchantId": "999"},
        )
        assert result == "99920260101120000sec"

    def test_url_details_extraction(self):
        data = {
            "merchantId": "1",
            "urlDetails": {"notificationUrl": "https://example.com/notify", "successUrl": "https://ok.com"},
        }
        fields = ["merchantId", "urlDetails", "secretKey"]
        result = build_checksum_string(data, fields, merchant_secret_key="k")
        assert result == "1https://example.com/notifyk"

    def test_billing_address_concatenation(self):
        data = {
            "billingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "address": "123 Main St",
                "phone": "555-0100",
                "zip": "10001",
                "city": "New York",
                "countryCode": "US",
                "state": "NY",
                "email": "john@test.com",
                "county": "",
            }
        }
        fields = ["billingAddress", "secretKey"]
        result = build_checksum_string(data, fields, merchant_secret_key="s")
        expected = "JohnDoe123 Main St555-010010001New YorkUSNYjohn@test.coms"
        assert result == expected

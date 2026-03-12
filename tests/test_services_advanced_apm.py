"""Tests for the Advanced APM service."""

from __future__ import annotations


class TestAddBankAccount:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.advanced_apm.add_bank_account(
            sessionToken="tok", userTokenId="u1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "addBankAccount"

    def test_injects_credentials(self, client, mock_request):
        client.advanced_apm.add_bank_account(sessionToken="tok")
        _, data = mock_request.call_args[0]
        assert data["merchantId"] == "test_mid"

    def test_no_checksum(self, client, mock_request):
        """Advanced APM endpoints use _inject_credentials, no checksum."""
        client.advanced_apm.add_bank_account(sessionToken="tok")
        _, data = mock_request.call_args[0]
        assert "checksum" not in data


class TestEnrollAccount:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.advanced_apm.enroll_account(
            sessionToken="tok", clientUniqueId="cu_1",
            userId="uid_1", userTokenId="u1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "enrollAccount"


class TestFundAccount:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.advanced_apm.fund_account(
            sessionToken="tok", clientUniqueId="cu_1", userId="uid_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "fundAccount"


class TestGetAccountDetails:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.advanced_apm.get_account_details(
            sessionToken="tok", clientUniqueId="cu_1", userId="uid_1",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getAccountDetails"


class TestGetDocumentUrl:
    def test_calls_correct_endpoint(self, client, mock_request):
        client.advanced_apm.get_document_url(
            sessionToken="tok", clientUniqueId="cu_1",
            documentType="terms",
        )
        endpoint, _ = mock_request.call_args[0]
        assert endpoint == "getDocumentUrl"

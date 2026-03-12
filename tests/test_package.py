"""Tests for package-level exports and version."""

from __future__ import annotations


class TestPackageExports:
    def test_version(self):
        import nuvei
        assert nuvei.__version__

    def test_all_exports_accessible(self):
        import nuvei

        for name in nuvei.__all__:
            assert hasattr(nuvei, name), f"Missing export: {name}"

    def test_all_list_complete(self):
        import nuvei
        expected = {
            "Nuvei", "AsyncNuvei",
            "Environment", "ServerConfig", "HashAlgorithm",
            "NuveiError", "APIError", "AuthenticationError",
            "ChecksumError", "TransportError", "ValidationError",
            "verify_webhook", "verify_webhook_generic",
            "calculate_checksum",
            "COUNTRY_CODES", "CURRENCIES", "LOCALES",
        }
        assert set(nuvei.__all__) == expected

    def test_hash_algorithm_type(self):
        """HashAlgorithm is a Literal type alias, importable."""
        from nuvei import HashAlgorithm
        assert HashAlgorithm is not None

    def test_constants_are_frozen(self):
        from nuvei import COUNTRY_CODES, CURRENCIES, LOCALES
        assert isinstance(COUNTRY_CODES, frozenset)
        assert isinstance(CURRENCIES, frozenset)
        assert isinstance(LOCALES, frozenset)
        assert "US" in COUNTRY_CODES
        assert "USD" in CURRENCIES
        assert "en_US" in LOCALES


class TestExceptionHierarchy:
    def test_api_error_is_nuvei_error(self):
        from nuvei import APIError, NuveiError
        assert issubclass(APIError, NuveiError)

    def test_auth_error_is_api_error(self):
        from nuvei import APIError, AuthenticationError
        assert issubclass(AuthenticationError, APIError)

    def test_transport_error_is_nuvei_error(self):
        from nuvei import NuveiError, TransportError
        assert issubclass(TransportError, NuveiError)

    def test_checksum_error_is_nuvei_error(self):
        from nuvei import ChecksumError, NuveiError
        assert issubclass(ChecksumError, NuveiError)

    def test_validation_error_is_nuvei_error(self):
        from nuvei import NuveiError, ValidationError
        assert issubclass(ValidationError, NuveiError)

    def test_api_error_attributes(self):
        from nuvei import APIError
        err = APIError(
            "test", err_code=1001, status="ERROR",
            reason="Bad request", response_body={"errCode": 1001},
        )
        assert err.err_code == 1001
        assert err.status == "ERROR"
        assert err.reason == "Bad request"
        assert err.response_body == {"errCode": 1001}
        assert str(err) == "test"

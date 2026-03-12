"""Tests for server configuration."""

from nuvei.config import Environment, ServerConfig


class TestServerConfig:
    def test_production_url(self):
        cfg = ServerConfig("prod")
        assert cfg.base_url == "https://secure.safecharge.com"
        assert cfg.environment == Environment.PRODUCTION

    def test_test_url(self):
        cfg = ServerConfig(Environment.TEST)
        assert cfg.base_url == "https://ppp-test.nuvei.com"

    def test_endpoint_generation(self):
        cfg = ServerConfig("test")
        url = cfg.endpoint("getSessionToken")
        assert url == "https://ppp-test.nuvei.com/ppp/api/v1/getSessionToken.do"

    def test_api_url(self):
        cfg = ServerConfig("prod")
        assert cfg.api_url == "https://secure.safecharge.com/ppp/api/v1"

    def test_case_insensitive(self):
        cfg = ServerConfig("TEST")
        assert cfg.environment == Environment.TEST

    def test_qa_url(self):
        cfg = ServerConfig("qa")
        assert cfg.base_url == "https://apmtest.gate2shop.com"

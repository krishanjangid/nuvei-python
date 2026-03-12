"""Environment configuration and API endpoint resolution."""

from __future__ import annotations

from enum import Enum


class Environment(str, Enum):
    PRODUCTION = "prod"
    TEST = "test"
    INTEGRATION = "int"
    QA = "qa"


_BASE_URLS: dict[str, str] = {
    Environment.PRODUCTION: "https://secure.safecharge.com",
    Environment.TEST: "https://ppp-test.nuvei.com",
    Environment.INTEGRATION: "https://ppp-test.nuvei.com",
    Environment.QA: "https://apmtest.gate2shop.com",
}

API_PATH = "/ppp/api/v1"


class ServerConfig:
    """Resolves the correct Nuvei API base URL for a given environment."""

    __slots__ = ("environment", "base_url")

    def __init__(self, environment: str | Environment = Environment.PRODUCTION) -> None:
        if isinstance(environment, str):
            environment = Environment(environment.lower())
        self.environment = environment
        self.base_url = _BASE_URLS[environment]

    @property
    def api_url(self) -> str:
        return f"{self.base_url}{API_PATH}"

    def endpoint(self, service: str) -> str:
        """Return the full URL for an API endpoint (e.g. 'payment' → '.../payment.do')."""
        return f"{self.api_url}/{service}.do"

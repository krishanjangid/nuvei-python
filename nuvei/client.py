"""Synchronous and asynchronous Nuvei API clients."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from .checksum import HashAlgorithm, build_checksum_string, calculate_checksum
from .config import Environment, ServerConfig
from .exceptions import APIError, AuthenticationError, TransportError

_SOURCE_APPLICATION = "PYTHON_SDK"

logger = logging.getLogger("nuvei")


def _timestamp() -> str:
    """Return current UTC time in ``YYYYMMDDHHmmss`` format."""
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d%H%M%S")


def _uuid() -> str:
    return str(uuid.uuid4())


class _ClientBase:
    """Shared configuration for both sync and async clients."""

    def __init__(
        self,
        merchant_id: str,
        merchant_site_id: str,
        merchant_secret_key: str,
        environment: str | Environment = Environment.PRODUCTION,
        *,
        algorithm: HashAlgorithm = "sha256",
        request_validation: bool = True,
        timeout: float = 30.0,
        auto_inject_ip: bool = False,
        source_application: str | None = None,
        web_master_id: str | None = None,
    ) -> None:
        self.merchant_id = str(merchant_id)
        self.merchant_site_id = str(merchant_site_id)
        self.merchant_secret_key = merchant_secret_key
        self.server_config = ServerConfig(environment)
        self.algorithm: HashAlgorithm = algorithm
        self.request_validation = request_validation
        self.timeout = timeout
        self.auto_inject_ip = auto_inject_ip
        self.source_application = source_application or _SOURCE_APPLICATION
        self.web_master_id = web_master_id or ""
        self._session_token: str | None = None

    @property
    def session_token(self) -> str | None:
        """Return the cached session token, if any."""
        return self._session_token

    # -- helpers exposed to service modules --

    def _inject_credentials(self, data: dict[str, Any]) -> dict[str, Any]:
        """Inject merchantId, merchantSiteId, clientRequestId, timeStamp,
        sourceApplication, and webMasterId."""
        data.setdefault("merchantId", self.merchant_id)
        data.setdefault("merchantSiteId", self.merchant_site_id)
        data.setdefault("clientRequestId", _uuid())
        data.setdefault("timeStamp", _timestamp())
        if self.source_application:
            data.setdefault("sourceApplication", self.source_application)
        if self.web_master_id:
            data.setdefault("webMasterId", self.web_master_id)
        return data

    def _sign(
        self,
        data: dict[str, Any],
        checksum_fields: list[str],
    ) -> dict[str, Any]:
        """Inject credentials and compute + attach checksum."""
        data = self._inject_credentials(data)
        raw = build_checksum_string(
            data,
            checksum_fields,
            merchant_secret_key=self.merchant_secret_key,
            self_data={
                "merchantId": self.merchant_id,
                "merchantSiteId": self.merchant_site_id,
            },
        )
        data["checksum"] = calculate_checksum([raw], algorithm=self.algorithm)
        return data

    def _cache_session_token(self, body: dict[str, Any]) -> None:
        """Cache the session token from a successful response."""
        token = body.get("sessionToken")
        if token:
            self._session_token = token

    @staticmethod
    def _handle_response(body: dict[str, Any], endpoint_name: str) -> dict[str, Any]:
        err_code = body.get("errCode", -1)
        status = body.get("status", "")

        if err_code != 0 and status == "ERROR":
            reason = body.get("reason", "Unknown error")
            exc_cls = AuthenticationError if endpoint_name == "getSessionToken" else APIError
            raise exc_cls(
                f"{endpoint_name} failed: {reason}",
                err_code=err_code,
                status=status,
                reason=reason,
                response_body=body,
            )
        return body


class Nuvei(_ClientBase):
    """Synchronous Nuvei API client.

    Usage::

        from nuvei import Nuvei

        client = Nuvei(
            merchant_id="...",
            merchant_site_id="...",
            merchant_secret_key="...",
            environment="test",
        )
        session = client.get_session_token()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._http = httpx.Client(timeout=self.timeout)

        from .services.advanced_apm import AdvancedAPMService
        from .services.authentication import AuthenticationService
        from .services.card_operations import CardOperationsService
        from .services.financial import FinancialService
        from .services.orders import OrderService
        from .services.payments import PaymentService
        from .services.subscriptions import SubscriptionService
        from .services.three_d_secure import ThreeDSecureService
        from .services.user_payment_options import UserPaymentOptionService
        from .services.users import UserService

        self.authentication = AuthenticationService(self)
        self.payments = PaymentService(self)
        self.financial = FinancialService(self)
        self.three_d_secure = ThreeDSecureService(self)
        self.card_operations = CardOperationsService(self)
        self.users = UserService(self)
        self.user_payment_options = UserPaymentOptionService(self)
        self.subscriptions = SubscriptionService(self)
        self.orders = OrderService(self)
        self.advanced_apm = AdvancedAPMService(self)

    # -- convenience shortcuts --

    def get_session_token(self, **kwargs: Any) -> dict[str, Any]:
        result = self.authentication.get_session_token(**kwargs)
        self._cache_session_token(result)
        return result

    def open_order(self, **kwargs: Any) -> dict[str, Any]:
        return self.orders.open_order(**kwargs)

    # -- low-level request --

    def request(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """POST *data* as JSON to the given *endpoint* and return the parsed response."""
        url = self.server_config.endpoint(endpoint)
        logger.debug("POST %s", url)
        try:
            resp = self._http.post(url, json=data)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("HTTP %s from %s", exc.response.status_code, endpoint)
            raise APIError(
                f"HTTP {exc.response.status_code} from {endpoint}",
                err_code=exc.response.status_code,
                response_body=exc.response.json() if exc.response.content else None,
            ) from exc
        except httpx.HTTPError as exc:
            logger.error("Transport error calling %s: %s", endpoint, exc)
            raise TransportError(f"Transport error calling {endpoint}: {exc}") from exc

        body = resp.json()
        logger.debug("Response from %s: status=%s errCode=%s", endpoint, body.get("status"), body.get("errCode"))
        return self._handle_response(body, endpoint)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Nuvei:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncNuvei(_ClientBase):
    """Asynchronous Nuvei API client (backed by ``httpx.AsyncClient``).

    Usage::

        import asyncio
        from nuvei import AsyncNuvei

        async def main():
            async with AsyncNuvei(
                merchant_id="...",
                merchant_site_id="...",
                merchant_secret_key="...",
                environment="test",
            ) as client:
                session = await client.get_session_token()

        asyncio.run(main())
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._http = httpx.AsyncClient(timeout=self.timeout)

        from .services.advanced_apm import AsyncAdvancedAPMService
        from .services.authentication import AsyncAuthenticationService
        from .services.card_operations import AsyncCardOperationsService
        from .services.financial import AsyncFinancialService
        from .services.orders import AsyncOrderService
        from .services.payments import AsyncPaymentService
        from .services.subscriptions import AsyncSubscriptionService
        from .services.three_d_secure import AsyncThreeDSecureService
        from .services.user_payment_options import AsyncUserPaymentOptionService
        from .services.users import AsyncUserService

        self.authentication = AsyncAuthenticationService(self)
        self.payments = AsyncPaymentService(self)
        self.financial = AsyncFinancialService(self)
        self.three_d_secure = AsyncThreeDSecureService(self)
        self.card_operations = AsyncCardOperationsService(self)
        self.users = AsyncUserService(self)
        self.user_payment_options = AsyncUserPaymentOptionService(self)
        self.subscriptions = AsyncSubscriptionService(self)
        self.orders = AsyncOrderService(self)
        self.advanced_apm = AsyncAdvancedAPMService(self)

    async def get_session_token(self, **kwargs: Any) -> dict[str, Any]:
        result = await self.authentication.get_session_token(**kwargs)
        self._cache_session_token(result)
        return result

    async def open_order(self, **kwargs: Any) -> dict[str, Any]:
        return await self.orders.open_order(**kwargs)

    async def request(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = self.server_config.endpoint(endpoint)
        logger.debug("POST %s", url)
        try:
            resp = await self._http.post(url, json=data)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("HTTP %s from %s", exc.response.status_code, endpoint)
            raise APIError(
                f"HTTP {exc.response.status_code} from {endpoint}",
                err_code=exc.response.status_code,
                response_body=exc.response.json() if exc.response.content else None,
            ) from exc
        except httpx.HTTPError as exc:
            logger.error("Transport error calling %s: %s", endpoint, exc)
            raise TransportError(f"Transport error calling {endpoint}: {exc}") from exc

        body = resp.json()
        logger.debug("Response from %s: status=%s errCode=%s", endpoint, body.get("status"), body.get("errCode"))
        return self._handle_response(body, endpoint)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncNuvei:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

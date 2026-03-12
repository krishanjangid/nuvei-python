"""Authentication service — ``/getSessionToken``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

SESSION_TOKEN_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "clientRequestId", "timeStamp", "secretKey",
]


class AuthenticationService:
    """Synchronous authentication operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def get_session_token(self, **kwargs: Any) -> dict[str, Any]:
        """Obtain a ``sessionToken`` (valid for 10 minutes).

        All keyword arguments are merged into the request body, allowing you
        to pass ``clientUniqueId`` or other optional fields.

        Returns the full API response dict which includes ``sessionToken``.
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, SESSION_TOKEN_CHECKSUM_FIELDS)
        return self._client.request("getSessionToken", data)


class AsyncAuthenticationService:
    """Asynchronous authentication operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def get_session_token(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, SESSION_TOKEN_CHECKSUM_FIELDS)
        return await self._client.request("getSessionToken", data)

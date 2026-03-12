"""User management — ``/createUser``, ``/updateUser``, ``/getUserDetails``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AsyncNuvei, Nuvei

USER_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "firstName", "lastName", "address", "state", "city", "zip",
    "countryCode", "phone", "locale", "email", "county",
    "timeStamp", "secretKey",
]

GET_USER_CHECKSUM_FIELDS = [
    "merchantId", "merchantSiteId", "userTokenId", "clientRequestId",
    "timeStamp", "secretKey",
]


class UserService:
    """Synchronous user management operations."""

    def __init__(self, client: Nuvei) -> None:
        self._client = client

    def create_user(self, **kwargs: Any) -> dict[str, Any]:
        """Register a new user in the Nuvei system (``/createUser``).

        Required kwargs:
            userTokenId, countryCode
        Optional:
            firstName, lastName, address, state, city, zip, phone,
            locale, email, dateOfBirth, county
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, USER_CHECKSUM_FIELDS)
        return self._client.request("createUser", data)

    def update_user(self, **kwargs: Any) -> dict[str, Any]:
        """Update an existing user's details (``/updateUser``).

        Required kwargs:
            userTokenId
        Optional:
            Any fields from ``create_user`` that need updating.
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, USER_CHECKSUM_FIELDS)
        return self._client.request("updateUser", data)

    def get_user_details(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a user's stored details (``/getUserDetails``).

        Required kwargs:
            userTokenId
        """
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_USER_CHECKSUM_FIELDS)
        return self._client.request("getUserDetails", data)


class AsyncUserService:
    """Asynchronous user management operations."""

    def __init__(self, client: AsyncNuvei) -> None:
        self._client = client

    async def create_user(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, USER_CHECKSUM_FIELDS)
        return await self._client.request("createUser", data)

    async def update_user(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, USER_CHECKSUM_FIELDS)
        return await self._client.request("updateUser", data)

    async def get_user_details(self, **kwargs: Any) -> dict[str, Any]:
        data: dict[str, Any] = {**kwargs}
        data = self._client._sign(data, GET_USER_CHECKSUM_FIELDS)
        return await self._client.request("getUserDetails", data)

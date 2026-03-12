"""Custom exception hierarchy for the Nuvei SDK."""

from __future__ import annotations

from typing import Any


class NuveiError(Exception):
    """Base exception for all Nuvei SDK errors."""

    def __init__(self, message: str, *, err_code: int = -1, details: Any = None) -> None:
        self.err_code = err_code
        self.details = details
        super().__init__(message)


class ValidationError(NuveiError):
    """Raised when request data fails schema validation before sending."""

    def __init__(self, message: str, *, errors: list[dict[str, Any]] | None = None) -> None:
        super().__init__(message, err_code=4001, details=errors)
        self.errors = errors or []


class APIError(NuveiError):
    """Raised when the Nuvei API returns an error response (errCode != 0)."""

    def __init__(
        self,
        message: str,
        *,
        err_code: int = -1,
        status: str | None = None,
        reason: str | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, err_code=err_code, details=response_body)
        self.status = status
        self.reason = reason
        self.response_body = response_body


class AuthenticationError(APIError):
    """Raised when session token retrieval or authentication fails."""


class TransportError(NuveiError):
    """Raised for HTTP-level transport failures (timeouts, connection errors)."""


class ChecksumError(NuveiError):
    """Raised when a checksum verification fails (e.g. webhook DMN validation)."""

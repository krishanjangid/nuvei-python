"""Nuvei REST API v1.0 SDK for Python.

Quickstart::

    from nuvei import Nuvei

    client = Nuvei(
        merchant_id="your_merchant_id",
        merchant_site_id="your_site_id",
        merchant_secret_key="your_secret_key",
        environment="test",  # "prod", "test", "int"
    )

    # Get session token
    session = client.get_session_token()
    token = session["sessionToken"]

    # Open an order
    order = client.open_order(amount="10.00", currency="USD")

For async usage::

    from nuvei import AsyncNuvei

    async with AsyncNuvei(...) as client:
        session = await client.get_session_token()
"""

from __future__ import annotations

from .checksum import HashAlgorithm, calculate_checksum
from .client import AsyncNuvei, Nuvei
from .config import Environment, ServerConfig
from .constants import COUNTRY_CODES, CURRENCIES, LOCALES
from .exceptions import (
    APIError,
    AuthenticationError,
    ChecksumError,
    NuveiError,
    TransportError,
    ValidationError,
)
from .webhook import verify_webhook, verify_webhook_generic

__all__ = [
    # Clients
    "Nuvei",
    "AsyncNuvei",
    # Config
    "Environment",
    "ServerConfig",
    "HashAlgorithm",
    # Exceptions
    "NuveiError",
    "APIError",
    "AuthenticationError",
    "ChecksumError",
    "TransportError",
    "ValidationError",
    # Webhooks
    "verify_webhook",
    "verify_webhook_generic",
    # Utilities
    "calculate_checksum",
    # Constants
    "COUNTRY_CODES",
    "CURRENCIES",
    "LOCALES",
]

__version__ = "1.0.0"

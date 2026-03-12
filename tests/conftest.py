"""Shared fixtures for Nuvei SDK tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from nuvei import Nuvei
from nuvei.client import AsyncNuvei


def _ok_response(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a standard success response body."""
    body: dict[str, Any] = {
        "status": "SUCCESS",
        "errCode": 0,
        "reason": "",
        "version": "1.0",
    }
    if extra:
        body.update(extra)
    return body


@pytest.fixture
def client():
    """Synchronous Nuvei client with a mocked HTTP transport."""
    c = Nuvei(
        merchant_id="test_mid",
        merchant_site_id="123456",
        merchant_secret_key="test_secret_key",
        environment="test",
    )
    yield c
    c.close()


@pytest.fixture
def async_client():
    """Asynchronous Nuvei client."""
    return AsyncNuvei(
        merchant_id="test_mid",
        merchant_site_id="123456",
        merchant_secret_key="test_secret_key",
        environment="test",
    )


@pytest.fixture
def mock_request(client, monkeypatch):
    """Patch the sync client's ``request`` method to return a configurable response."""
    response_data = _ok_response({"sessionToken": "tok_abc123"})
    mock = MagicMock(return_value=response_data)
    monkeypatch.setattr(client, "request", mock)
    return mock


@pytest.fixture
def make_ok_response():
    """Factory to build OK response dicts."""
    return _ok_response

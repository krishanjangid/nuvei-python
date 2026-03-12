"""SHA-256 / MD5 checksum calculation for Nuvei API authentication."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from typing import Any, Literal

HashAlgorithm = Literal["sha256", "md5"]


def calculate_checksum(
    values: Sequence[str],
    algorithm: HashAlgorithm = "sha256",
) -> str:
    """Concatenate *values* with no separator and return the hex digest.

    Args:
        values: Ordered field values to concatenate.
        algorithm: ``"sha256"`` (default) or ``"md5"``.
    """
    raw = "".join(str(v) for v in values)
    return hashlib.new(algorithm, raw.encode("utf-8")).hexdigest()


def build_checksum_string(
    data: dict[str, Any],
    fields: Sequence[str],
    *,
    merchant_secret_key: str,
    self_data: dict[str, Any] | None = None,
) -> str:
    """Build the concatenated string for checksum hashing.

    For each field in *fields*, the value is taken from *data* first,
    then from *self_data* (merchant-level defaults), falling back to ``""``.
    The special key ``"secretKey"`` is resolved to *merchant_secret_key*.
    For ``"urlDetails"``, only the ``notificationUrl`` sub-field is used.
    For ``"billingAddress"``, sub-fields are concatenated in Nuvei's prescribed order.
    """
    self_data = self_data or {}
    parts: list[str] = []

    for field in fields:
        if field == "secretKey":
            parts.append(merchant_secret_key)
            continue

        value = data.get(field, self_data.get(field, ""))

        if field == "urlDetails" and isinstance(value, dict):
            value = value.get("notificationUrl", "")
        elif field == "billingAddress" and isinstance(value, dict):
            ba_fields = [
                "firstName", "lastName", "address", "phone", "zip",
                "city", "countryCode", "state", "email", "county",
            ]
            value = "".join(str(value.get(f, "")) for f in ba_fields)

        parts.append(str(value) if value else "")

    return "".join(parts)

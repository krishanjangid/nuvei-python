"""Webhook (DMN — Direct Merchant Notification) verification.

Nuvei sends DMN callbacks to your server after transaction events.
Each DMN includes an ``advanceResponseChecksum`` that you must verify
to ensure the notification is authentic and has not been tampered with.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

from .checksum import HashAlgorithm
from .exceptions import ChecksumError


def verify_webhook(
    params: dict[str, Any],
    merchant_secret_key: str,
    *,
    algorithm: HashAlgorithm = "sha256",
    raise_on_failure: bool = True,
) -> bool:
    """Verify the ``advanceResponseChecksum`` in a Nuvei DMN (webhook).

    Nuvei computes the checksum by concatenating specific DMN parameter values
    in order and hashing with the merchant's secret key appended.

    The standard concatenation order for payment DMNs is::

        merchantSecretKey + totalAmount + currency + responseTimeStamp
        + PPP_TransactionID + Status + productId

    Args:
        params: The DMN callback parameters (query string or POST body).
        merchant_secret_key: Your merchant secret key.
        algorithm: Hash algorithm (``"sha256"`` or ``"md5"``).
        raise_on_failure: If *True*, raise :class:`ChecksumError` on mismatch.

    Returns:
        *True* if the checksum is valid.

    Raises:
        ChecksumError: If verification fails and *raise_on_failure* is *True*.
    """
    received_checksum = params.get("advanceResponseChecksum", "")
    if not received_checksum:
        if raise_on_failure:
            raise ChecksumError("No advanceResponseChecksum found in DMN params")
        return False

    raw = "".join(
        str(params.get(field, ""))
        for field in _DMN_CHECKSUM_FIELDS
    )
    raw = merchant_secret_key + raw

    computed = hashlib.new(algorithm, raw.encode("utf-8")).hexdigest()

    is_valid = hmac.compare_digest(computed, received_checksum)

    if not is_valid and raise_on_failure:
        raise ChecksumError("DMN checksum verification failed")

    return is_valid


def verify_webhook_generic(
    params: dict[str, Any],
    merchant_secret_key: str,
    checksum_fields: list[str],
    *,
    checksum_param: str = "advanceResponseChecksum",
    algorithm: HashAlgorithm = "sha256",
    secret_position: str = "prefix",
    raise_on_failure: bool = True,
) -> bool:
    """Generic DMN verification with custom field ordering.

    Some DMN types use different field orderings. Use this function when you
    need to specify the exact concatenation order.

    Args:
        params: The DMN callback parameters.
        merchant_secret_key: Your merchant secret key.
        checksum_fields: Ordered list of DMN parameter names to concatenate.
        checksum_param: Name of the checksum parameter in *params*.
        algorithm: Hash algorithm.
        secret_position: ``"prefix"`` or ``"suffix"`` — where to place the secret key.
        raise_on_failure: If *True*, raise on mismatch.
    """
    received_checksum = params.get(checksum_param, "")
    if not received_checksum:
        if raise_on_failure:
            raise ChecksumError(f"No {checksum_param} found in DMN params")
        return False

    parts = [str(params.get(f, "")) for f in checksum_fields]

    if secret_position == "prefix":
        raw = merchant_secret_key + "".join(parts)
    else:
        raw = "".join(parts) + merchant_secret_key

    computed = hashlib.new(algorithm, raw.encode("utf-8")).hexdigest()
    is_valid = hmac.compare_digest(computed, received_checksum)

    if not is_valid and raise_on_failure:
        raise ChecksumError("DMN checksum verification failed")

    return is_valid


_DMN_CHECKSUM_FIELDS = [
    "totalAmount",
    "currency",
    "responseTimeStamp",
    "PPP_TransactionID",
    "Status",
    "productId",
]

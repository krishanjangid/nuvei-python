# Nuvei Python SDK

[![Downloads](https://static.pepy.tech/personalized-badge/nuvei?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/nuvei)
[![pypi](https://img.shields.io/pypi/v/nuvei?label=latest%20version)](https://pypi.org/project/nuvei/)
[![Python](https://img.shields.io/pypi/pyversions/nuvei)](https://pypi.org/project/nuvei/)
[![CI](https://img.shields.io/github/actions/workflow/status/krishanjangid/nuvei-python/ci.yml?label=CI)](https://github.com/krishanjangid/nuvei-python/actions/workflows/ci.yml)
[![Issues](https://img.shields.io/github/issues-raw/krishanjangid/nuvei-python)](https://github.com/krishanjangid/nuvei-python/issues)
[![Contributors](https://img.shields.io/github/contributors/krishanjangid/nuvei-python)](https://github.com/krishanjangid/nuvei-python/graphs/contributors)
[![License](https://img.shields.io/pypi/l/nuvei)](https://github.com/krishanjangid/nuvei-python/blob/main/LICENSE)
[![GitHub Follows](https://img.shields.io/github/followers/krishanjangid?label=Github%20Follows)](https://github.com/krishanjangid)

A lightweight Python wrapper for the **Nuvei REST API v1.0** — authentication, payments, 3D Secure, financial operations, subscriptions, user & payment option management, all in one package.

**Requires Python 3.9+**

---

### Quick Links

- [Features](#features) · [Installation](#installation) · [Quick Start](#quick-start) · [Service Modules](#service-modules)
- [Integration Flows](#integration-flows) · [Webhook Verification](#webhook-dmn-verification) · [Configuration](#configuration)
- [Error Handling](#error-handling) · [Testing & Development](#testing--development) · [Helpful Resources](#helpful-resources)
- [Contributing](#contributing) · [Changelog](#changelog) · [License](#license)

---

## Features

- **Full API v1.0 coverage** — authentication, payments, financial operations, 3D Secure, card operations, subscriptions, user & UPO management, advanced APM
- **Sync and async clients** — powered by `httpx`
- **Automatic checksum calculation** — SHA-256 (default) or MD5
- **Webhook/DMN verification** — validate `advanceResponseChecksum` on incoming notifications
- **Type-annotated** — full type hints with `py.typed` marker (PEP 561)
- **Minimal dependencies** — only `httpx`

## Installation

```bash
pip install nuvei
```

Or for development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Synchronous Usage

```python
from nuvei import Nuvei

client = Nuvei(
    merchant_id="your_merchant_id",
    merchant_site_id="your_site_id",
    merchant_secret_key="your_secret_key",
    environment="test",  # "prod", "test", "int", "qa"
)

# 1. Get a session token
session = client.get_session_token()
token = session["sessionToken"]

# 2. Open an order
order = client.open_order(amount="10.00", currency="USD")
order_token = order["sessionToken"]

# 3. Process a payment
result = client.payments.payment(
    sessionToken=order_token,
    amount="10.00",
    currency="USD",
    paymentOption={
        "card": {
            "cardNumber": "4111111111111111",
            "cardHolderName": "John Doe",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
        }
    },
)
print(result["transactionId"], result["status"])
```

### Async Usage

```python
import asyncio
from nuvei import AsyncNuvei

async def main():
    async with AsyncNuvei(
        merchant_id="your_merchant_id",
        merchant_site_id="your_site_id",
        merchant_secret_key="your_secret_key",
        environment="test",
    ) as client:
        session = await client.get_session_token()
        print(session["sessionToken"])

asyncio.run(main())
```

## Service Modules

Access API endpoints through organized service namespaces:

| Service | Accessor | Endpoints |
|---------|----------|-----------|
| **Authentication** | `client.authentication` | `get_session_token` |
| **Orders** | `client.orders` | `open_order`, `update_order`, `get_order_details` |
| **Payments** | `client.payments` | `payment`, `payment_cc`, `payment_apm`, `init_payment`, `get_payment_status`, `account_capture`, `get_mcp_rates`, `get_dcc_details` |
| **Financial** | `client.financial` | `settle_transaction`, `refund_transaction`, `void_transaction`, `payout`, `get_payout_status` |
| **3D Secure** | `client.three_d_secure` | `authorize3d`, `verify3d`, `dynamic3d` |
| **Card Operations** | `client.card_operations` | `card_tokenization`, `get_card_details` |
| **Users** | `client.users` | `create_user`, `update_user`, `get_user_details` |
| **UPOs** | `client.user_payment_options` | `add_upo_credit_card`, `add_upo_credit_card_by_temp_token`, `add_upo_credit_card_by_token`, `add_upo_apm`, `edit_upo_cc`, `edit_upo_apm`, `get_user_upos`, `delete_upo`, `suspend_upo`, `enable_upo`, `get_merchant_payment_methods` |
| **Subscriptions** | `client.subscriptions` | `create_plan`, `edit_plan`, `get_plans_list`, `create_subscription`, `edit_subscription`, `cancel_subscription`, `get_subscriptions_list`, `get_subscription_plans` |
| **Advanced APM** | `client.advanced_apm` | `add_bank_account`, `enroll_account`, `fund_account`, `get_account_details`, `get_document_url` |

---

## Integration Flows

### Flow 1: Simple Payment (Sale)

The most common flow — charge a customer immediately.

```python
from nuvei import Nuvei

client = Nuvei(
    merchant_id="...", merchant_site_id="...",
    merchant_secret_key="...", environment="test",
)

# Step 1: Open an order
order = client.open_order(amount="29.99", currency="USD")

# Step 2: Process the payment
result = client.payments.payment(
    sessionToken=order["sessionToken"],
    amount="29.99",
    currency="USD",
    transactionType="Sale",
    paymentOption={
        "card": {
            "cardNumber": "4111111111111111",
            "cardHolderName": "Jane Smith",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
        }
    },
    deviceDetails={"ipAddress": "192.168.1.1"},
)

if result["status"] == "SUCCESS" and result["transactionStatus"] == "APPROVED":
    print(f"Payment approved! Transaction ID: {result['transactionId']}")
```

### Flow 2: Auth and Settle

Authorize first, then settle (capture) later — common for e-commerce.

```python
# Step 1: Open order
order = client.open_order(amount="100.00", currency="USD")

# Step 2: Authorize (hold funds, don't charge yet)
auth = client.payments.payment(
    sessionToken=order["sessionToken"],
    amount="100.00",
    currency="USD",
    transactionType="Auth",
    paymentOption={
        "card": {
            "cardNumber": "4111111111111111",
            "cardHolderName": "John Doe",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
        }
    },
)

# Step 3: Settle (capture) — can be full or partial amount
settle = client.financial.settle_transaction(
    relatedTransactionId=auth["transactionId"],
    amount="100.00",  # or a partial amount like "50.00"
    currency="USD",
    authCode=auth["authCode"],
)
```

### Flow 3: Payment with 3D Secure (3DS 2.0)

Full 3DS flow for liability-shifted payments.

```python
# Step 1: Open order
order = client.open_order(amount="50.00", currency="USD")

# Step 2: Init payment — check 3DS support
init = client.payments.init_payment(
    sessionToken=order["sessionToken"],
    amount="50.00",
    currency="USD",
    paymentOption={
        "card": {
            "cardNumber": "4000027891380961",  # 3DS test card
            "cardHolderName": "CL-BRW1",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
            "threeD": {
                "methodNotificationUrl": "https://your-site.com/3ds-notify",
            },
        }
    },
)

# Step 3: Handle 3DS fingerprinting (client-side iframe)
# Render the threeD data from init["paymentOption"]["card"]["threeD"]

# Step 4: Authorize 3D (after challenge completion)
auth3d = client.three_d_secure.authorize3d(
    sessionToken=order["sessionToken"],
    amount="50.00",
    currency="USD",
    paymentOption={
        "card": {
            "threeD": {
                # Include challenge result data here
            }
        }
    },
    relatedTransactionId=init["transactionId"],
)

# Step 5: Final payment with liability shift
payment = client.payments.payment(
    sessionToken=order["sessionToken"],
    amount="50.00",
    currency="USD",
    transactionType="Sale",
    relatedTransactionId=auth3d["transactionId"],
    paymentOption={
        "card": {
            "cardNumber": "4000027891380961",
            "cardHolderName": "CL-BRW1",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
        }
    },
)
```

### Flow 4: Returning Customer (CIT / MIT with UPO)

Save a payment method after the first transaction, then use it for future payments.

```python
# --- First-time payment: Customer-Initiated Transaction (CIT) ---

# Step 1: Create the user
client.users.create_user(
    userTokenId="customer_12345",
    countryCode="US",
    firstName="Jane",
    lastName="Smith",
    email="jane@example.com",
)

# Step 2: Open order with userTokenId
order = client.open_order(
    amount="49.99", currency="USD",
    userTokenId="customer_12345",
)

# Step 3: Process first payment (card is saved automatically with userTokenId)
first_payment = client.payments.payment(
    sessionToken=order["sessionToken"],
    amount="49.99",
    currency="USD",
    transactionType="Sale",
    userTokenId="customer_12345",
    paymentOption={
        "card": {
            "cardNumber": "4111111111111111",
            "cardHolderName": "Jane Smith",
            "expirationMonth": "12",
            "expirationYear": "2028",
            "CVV": "217",
        }
    },
)

# Step 4: Get saved payment methods (UPOs)
upos = client.user_payment_options.get_user_upos(
    userTokenId="customer_12345",
)
upo_id = upos["paymentMethods"][0]["userPaymentOptionId"]

# --- Future payment: Use saved UPO (CIT or MIT) ---

order2 = client.open_order(
    amount="49.99", currency="USD",
    userTokenId="customer_12345",
)

future_payment = client.payments.payment(
    sessionToken=order2["sessionToken"],
    amount="49.99",
    currency="USD",
    transactionType="Sale",
    userTokenId="customer_12345",
    paymentOption={"userPaymentOptionId": upo_id},
    isRebilling="0",  # "1" for MIT (merchant-initiated)
)
```

### Flow 5: Subscription / Rebilling

Set up automatic recurring payments.

```python
# Step 1: Create a plan
plan = client.subscriptions.create_plan(
    name="Premium Monthly",
    initialAmount="0.00",
    recurringAmount="29.99",
    currency="USD",
    endAfter={"day": "0", "month": "12", "year": "0"},
    startAfter={"day": "0", "month": "1", "year": "0"},
)

# Step 2: Create a subscription for the user
sub = client.subscriptions.create_subscription(
    userTokenId="customer_12345",
    planId=plan["planId"],
    userPaymentOptionId=upo_id,
    initialAmount="0.00",
    recurringAmount="29.99",
    currency="USD",
    endAfter={"day": "0", "month": "12", "year": "0"},
)

# Step 3: List active subscriptions
subs = client.subscriptions.get_subscriptions_list(
    userTokenId="customer_12345",
    subscriptionStatus="ACTIVE",
)

# Step 4: Cancel when needed
client.subscriptions.cancel_subscription(
    subscriptionId=sub["subscriptionId"],
)
```

### Flow 6: Refund

```python
# Full refund
refund = client.financial.refund_transaction(
    relatedTransactionId="original_txn_id",
    amount="49.99",
    currency="USD",
    clientUniqueId="refund-001",
    authCode="original_auth_code",
)

# Partial refund
partial_refund = client.financial.refund_transaction(
    relatedTransactionId="original_txn_id",
    amount="10.00",  # partial amount
    currency="USD",
    clientUniqueId="refund-002",
    authCode="original_auth_code",
)
```

### Flow 7: Void

Cancel a transaction before settlement.

```python
void = client.financial.void_transaction(
    relatedTransactionId="original_txn_id",
    amount="49.99",
    currency="USD",
    authCode="original_auth_code",
)
```

### Flow 8: Payout

Send money to a payment method (credit/disbursement).

```python
payout = client.financial.payout(
    userTokenId="customer_12345",
    amount="100.00",
    currency="USD",
    userPaymentOption={"userPaymentOptionId": upo_id},
    comment="Withdrawal payout",
)

# Check payout status
status = client.financial.get_payout_status(
    clientRequestId=payout["clientRequestId"],
)
```

---

## Webhook (DMN) Verification

Nuvei sends Direct Merchant Notifications (DMN) to your server after transaction events. Always verify the checksum.

```python
from nuvei import verify_webhook

# In your webhook handler (Flask, FastAPI, Django, etc.)
def handle_nuvei_webhook(params: dict):
    is_valid = verify_webhook(
        params,
        merchant_secret_key="your_secret_key",
        raise_on_failure=False,  # or True to raise ChecksumError
    )
    if is_valid:
        txn_id = params.get("PPP_TransactionID")
        status = params.get("Status")
        # Process the notification...
```

For custom DMN types with different field orderings:

```python
from nuvei import verify_webhook_generic

verify_webhook_generic(
    params,
    merchant_secret_key="your_secret_key",
    checksum_fields=["fieldA", "fieldB", "fieldC"],
    checksum_param="advanceResponseChecksum",
    secret_position="prefix",  # or "suffix"
)
```

---

## Configuration

### Hash Algorithm

```python
# Default is SHA-256; switch to MD5 if your account requires it
client = Nuvei(..., algorithm="md5")
```

### Environments

| Environment | Base URL |
|-------------|----------|
| `prod` | `https://secure.safecharge.com` |
| `test` | `https://ppp-test.nuvei.com` |
| `int` | `https://ppp-test.nuvei.com` |
| `qa` | `https://apmtest.gate2shop.com` |

### Context Manager

```python
# Auto-close the HTTP client
with Nuvei(...) as client:
    session = client.get_session_token()
```

---

## Error Handling

The SDK raises specific exceptions for different failure modes:

```python
from nuvei import APIError, AuthenticationError, TransportError, ChecksumError

try:
    result = client.payments.payment(...)
except AuthenticationError as e:
    # Session token or credential issues
    print(f"Auth failed: {e.reason}")
except APIError as e:
    # Nuvei API returned an error
    print(f"API error {e.err_code}: {e.reason}")
    print(e.response_body)  # full response dict
except TransportError as e:
    # Network / HTTP-level errors
    print(f"Network error: {e}")
```

### Response Handling

Every API method returns the full response dict from Nuvei. Check these fields:

| Field | Description |
|-------|-------------|
| `status` | `"SUCCESS"` or `"ERROR"` — indicates if the request was processed |
| `errCode` | `0` for success, non-zero for errors |
| `reason` | Human-readable error description |
| `transactionStatus` | `"APPROVED"`, `"DECLINED"`, `"PENDING"`, `"ERROR"` — actual transaction result |
| `transactionId` | Nuvei's unique transaction identifier |
| `authCode` | Authorization code from the issuer |
| `gwErrorCode` | Gateway-specific error code |
| `gwErrorReason` | Gateway-specific error description |

> **Important**: A `status: "SUCCESS"` means the request was processed — it does NOT mean the transaction was approved. Always check `transactionStatus` for the actual result.

For more details, see: [Nuvei Response Handling Guide](https://docs.nuvei.com/documentation/integration/response-handling/)

---

## Testing & Development

### Running Tests

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

### Testing Cards

Use these test card numbers in the **test** environment:

| Card Number | Brand | Behavior |
|-------------|-------|----------|
| `4111111111111111` | Visa | Approved |
| `5111111111111118` | Mastercard | Approved |
| `4000027891380961` | Visa | 3DS Challenge |
| `4000020951595032` | Visa | 3DS Frictionless |
| `4000023104662535` | Visa | Declined |

- **Expiry date**: Any future date (e.g. `12/2028`)
- **CVV**: Any 3 digits (e.g. `217`)

For the full list of testing cards, see: [Nuvei Testing Cards](https://docs.nuvei.com/documentation/integration/testing/testing-cards/)

### Testing with Postman

Nuvei provides a Postman collection for testing API calls interactively:

1. Import the Nuvei API collection into Postman
2. Set environment variables: `merchantId`, `merchantSiteId`, `merchantSecretKey`
3. Use the collection to test individual endpoints and verify responses

For details, see: [Testing APIs with Postman](https://docs.nuvei.com/documentation/integration/testing/testing-apis-with-postman/)

---

## Helpful Resources

| Resource | Link |
|----------|------|
| **Nuvei API v1.0 Reference** | [Main API Docs](https://docs.nuvei.com/api/main/indexMain_v1_0.html?json#Introduction) |
| **Advanced API Reference** | [Advanced API Docs](https://docs.nuvei.com/api/advanced/indexAdvanced.html?json#Introduction) |
| **Response Handling** | [Response Handling Guide](https://docs.nuvei.com/documentation/integration/response-handling/) |
| **Webhooks (DMN)** | [Webhook Documentation](https://docs.nuvei.com/documentation/integration/webhooks/) |
| **Testing Cards** | [Testing Cards Reference](https://docs.nuvei.com/documentation/integration/testing/testing-cards/) |
| **Testing with Postman** | [Postman Guide](https://docs.nuvei.com/documentation/integration/testing/testing-apis-with-postman/) |
| **3D Secure** | [3DS Documentation](https://docs.nuvei.com/documentation/features/3d-secure/) |
| **Financial Operations** | [Financial Ops Guide](https://docs.nuvei.com/documentation/features/financial-operations/) |
| **Subscription/Rebilling** | [Subscription Docs](https://docs.nuvei.com/documentation/features/subscription-rebilling/) |
| **Authentication** | [Auth Documentation](https://docs.nuvei.com/documentation/features/authentication/) |
| **Checksum Tool** | [Online Checksum Calculator](https://docs.nuvei.com/checksum-tool/) |

---

## Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the SDK:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes and add tests
4. Open a pull request

For bugs or questions, [open an issue](https://github.com/krishanjangid/nuvei-python/issues).

---

## Changelog

See [CHANGELOG.md](https://github.com/krishanjangid/nuvei-python/blob/main/CHANGELOG.md) for a full list of changes in each release.

---

## License

MIT — see [LICENSE](https://github.com/krishanjangid/nuvei-python/blob/main/LICENSE) for details.

---

<p align="center">
  Made with Python & ❤️ by <a href="https://github.com/krishanjangid">KK Jangid</a>
</p>

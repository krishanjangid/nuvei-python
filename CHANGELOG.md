# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.2] - 2026-03-12

### Improved

- Updated README badges: pepy.tech total downloads, latest version label, raw issue count, contributor count, GitHub follows

## [1.0.1] - 2026-03-12

### Improved

- Added shields.io badges (PyPI version, Python versions, license, CI status)
- Added quick links / table of contents for easier navigation
- Added Python version requirement note
- Added contributing guide with issue link
- Added changelog reference section
- Added footer attribution

## [1.0.0] - 2026-03-12

### Added

- Sync and async clients (`Nuvei`, `AsyncNuvei`) powered by `httpx`
- Authentication: `getSessionToken`
- Orders: `openOrder`, `updateOrder`, `getOrderDetails`
- Payments: `payment`, `paymentCC`, `paymentAPM`, `initPayment`, `getPaymentStatus`, `accountCapture`, `getMcpRates`, `getDccDetails`
- Financial operations: `settleTransaction`, `refundTransaction`, `voidTransaction`, `payout`, `getPayoutStatus`
- 3D Secure: `authorize3d`, `verify3d`, `dynamic3D`
- Card operations: `cardTokenization`, `getCardDetails`
- User management: `createUser`, `updateUser`, `getUserDetails`
- UPO management: `addUPOCreditCard`, `addUPOCreditCardByTempToken`, `addUPOCreditCardByToken`, `addUPOAPM`, `editUPOCC`, `editUPOAPM`, `getUserUPOs`, `deleteUPO`, `suspendUPO`, `enableUPO`, `getMerchantPaymentMethods`
- Subscriptions: `createPlan`, `editPlan`, `getPlansList`, `createSubscription`, `editSubscription`, `cancelSubscription`, `getSubscriptionsList`, `getSubscriptionPlans`
- Advanced APM: `addBankAccount`, `enrollAccount`, `fundAccount`, `getAccountDetails`, `getDocumentUrl`
- Webhook/DMN verification (`verify_webhook`, `verify_webhook_generic`)
- SHA-256 and MD5 checksum support
- Full type annotations with `py.typed` marker (PEP 561)
- Comprehensive test suite (183 tests)

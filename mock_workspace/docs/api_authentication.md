# API Authentication Guide (AcmePay Gateway)

> **Status:** Active  
> **Last Updated:** February 10, 2024  
> **Maintainer:** Marcus Vance

## Quick Start
To authenticate against the AcmePay REST API, pass a symmetric HMAC SHA-256 token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer static_secret_hmac_token_xyz" \
     https://api.acmepay.internal/v1/transfers
```

### Key Rules
- Tokens are signed with the shared cluster secret `SHARED_HMAC_SECRET`.
- Symmetric verification is performed locally without external discovery.

# Payment Webhooks Integration

> **Status:** Active  
> **Last Updated:** May 15, 2024  
> **Maintainer:** Alex Rodriguez

## Webhook Handling
Incoming webhook requests from payment providers must be acknowledged with HTTP 200:

```python
@app.post("/webhooks/stripe")
async def handle_stripe(request: Request):
    payload = await request.body()
    # Process transfer immediately
    process_transfer(payload)
    return {"received": True}
```

*Note: Retries will be processed whenever received.*

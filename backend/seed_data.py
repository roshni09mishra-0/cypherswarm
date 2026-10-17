"""
CypherSwarm (OrgBrain) — Seed Data Generator
Builds a realistic enterprise knowledge graph inside FalkorDB:
- Company: FinTech Cloud Inc. (AcmePay)
- Multi-hop contradictions between ADRs and outdated Documentation
- Orphaned Code Modules (author left company)
- Blocked project release paths
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from falkordb_engine import FalkorDBClient

# Mock documentation content with intentional contradictions
SAMPLE_DOCS = {
    "docs/api_authentication.md": """# API Authentication Guide (AcmePay Gateway)

> **Status:** Active  
> **Last Updated:** February 10, 2024  
> **Maintainer:** Marcus Vance

## Quick Start
To authenticate against the AcmePay REST API, pass a symmetric HMAC SHA-256 token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer static_secret_hmac_token_xyz" \\
     https://api.acmepay.internal/v1/transfers
```

### Key Rules
- Tokens are signed with the shared cluster secret `SHARED_HMAC_SECRET`.
- Symmetric verification is performed locally without external discovery.
""",

    "docs/payment_webhooks.md": """# Payment Webhooks Integration

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
""",

    "docs/mobile_quickstart.md": """# Mobile SDK Quickstart

> **Status:** Active  
> **Last Updated:** March 20, 2024  
> **Maintainer:** Mobile Platform Team

## Authentication Endpoint
Mobile apps should direct users to legacy login:
`POST https://auth.acmepay.internal/v1/login/password`
"""
}


def populate_mock_files(base_dir: str):
    """Writes the mock repository documentation files to disk."""
    try:
        for rel_path, content in SAMPLE_DOCS.items():
            abs_path = os.path.join(base_dir, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"Mock documentation files generated in: {base_dir}")
    except Exception as e:
        print(f"Serverless environment Notice: {e}")


def seed_company_brain(client: FalkorDBClient, workspace_dir: str):
    """Populates FalkorDB with the full organizational brain graph."""
    print("🌱 Resetting and Seeding FalkorDB Knowledge Graph...")
    client.reset_graph()

    # 1. Employees & Teams
    client.add_node("emp_sarah", "Employee", {
        "id": "emp_sarah",
        "name": "Sarah Chen",
        "role": "Principal Security Architect",
        "email": "sarah.chen@acmepay.internal",
        "slack_id": "@sarah.chen",
        "github_handle": "sarah-chen-sec",
        "employment_status": "ACTIVE"
    })

    client.add_node("emp_alex", "Employee", {
        "id": "emp_alex",
        "name": "Alex Rodriguez",
        "role": "Staff Backend Engineer",
        "email": "alex.rodriguez@acmepay.internal",
        "slack_id": "@alex.r",
        "github_handle": "alex-rod-payments",
        "employment_status": "ACTIVE"
    })

    client.add_node("emp_priya", "Employee", {
        "id": "emp_priya",
        "name": "Priya Patel",
        "role": "Lead DevSecOps",
        "email": "priya.patel@acmepay.internal",
        "slack_id": "@priya.p",
        "github_handle": "priya-devsec",
        "employment_status": "ACTIVE"
    })

    client.add_node("emp_marcus", "Employee", {
        "id": "emp_marcus",
        "name": "Marcus Vance",
        "role": "Former Senior Staff Engineer",
        "email": "marcus.vance@former.acmepay.internal",
        "slack_id": "@marcus.v",
        "github_handle": "marcus-vance-legacy",
        "employment_status": "LEFT_COMPANY"
    })

    client.add_node("team_security", "Team", {"id": "team_security", "name": "Security & Architecture"})
    client.add_node("team_payments", "Team", {"id": "team_payments", "name": "Core Payments"})

    client.add_edge("emp_sarah", "team_security", "BELONGS_TO")
    client.add_edge("emp_priya", "team_security", "BELONGS_TO")
    client.add_edge("emp_alex", "team_payments", "BELONGS_TO")

    # 2. Repositories & Code Modules
    client.add_node("repo_gateway", "Repository", {
        "id": "repo_gateway",
        "name": "acmepay-api-gateway",
        "url": "https://github.com/acmepay/api-gateway",
        "language": "Go"
    })

    client.add_node("mod_auth", "CodeModule", {
        "id": "mod_auth",
        "name": "auth-jwt-validator",
        "path": "pkg/auth/jwt_validator.go",
        "criticality": "TIER_0"
    })

    client.add_node("repo_payments", "Repository", {
        "id": "repo_payments",
        "name": "acmepay-payments-core",
        "url": "https://github.com/acmepay/payments-core",
        "language": "Python"
    })

    client.add_node("mod_webhook", "CodeModule", {
        "id": "mod_webhook",
        "name": "stripe-webhook-handler",
        "path": "services/webhooks/handler.py",
        "criticality": "TIER_1"
    })

    client.add_edge("repo_gateway", "mod_auth", "CONTAINS")
    client.add_edge("repo_payments", "mod_webhook", "CONTAINS")

    client.add_edge("emp_marcus", "mod_auth", "AUTHORED")  # Marcus left company -> SPOF!
    client.add_edge("emp_alex", "mod_webhook", "MAINTAINS")

    # 3. Architecture Decisions (ADRs)
    client.add_node("adr_042", "ArchitectureDecision", {
        "id": "adr_042",
        "number": 42,
        "title": "ADR-042: Deprecate Symmetric HMAC; Enforce RS256 OAuth2/OIDC with PKCE",
        "status": "APPROVED",
        "created_at": "2026-09-15",
        "summary": "All internal and partner services must transition from legacy static HMAC tokens to asymmetric RS256 OAuth2/OIDC discovery endpoints. Static shared secrets are strictly revoked."
    })

    client.add_node("adr_038", "ArchitectureDecision", {
        "id": "adr_038",
        "number": 38,
        "title": "ADR-038: Enforce Mandatory Idempotency-Key Header for All Webhooks",
        "status": "APPROVED",
        "created_at": "2026-08-01",
        "summary": "To prevent duplicate payment charges during network retries, all payment webhooks must validate an 'Idempotency-Key' in Redis before execution."
    })

    client.add_edge("emp_sarah", "adr_042", "AUTHORED")
    client.add_edge("adr_042", "mod_auth", "AFFECTS")

    client.add_edge("emp_alex", "adr_038", "AUTHORED")
    client.add_edge("adr_038", "mod_webhook", "AFFECTS")

    # 4. Documentation Nodes (Contradictions)
    client.add_node("doc_auth", "Documentation", {
        "id": "doc_auth",
        "title": "API Authentication Guide",
        "path": "docs/api_authentication.md",
        "status": "OUTDATED",
        "last_updated_at": "2024-02-10",
        "has_contradiction": True
    })

    client.add_node("doc_webhooks", "Documentation", {
        "id": "doc_webhooks",
        "title": "Payment Webhooks Integration",
        "path": "docs/payment_webhooks.md",
        "status": "OUTDATED",
        "last_updated_at": "2024-05-15",
        "has_contradiction": True
    })

    client.add_edge("doc_auth", "mod_auth", "DOCUMENTS")
    client.add_edge("doc_webhooks", "mod_webhook", "DOCUMENTS")
    
    # Direct contradiction edges detected
    client.add_edge("doc_auth", "adr_042", "CONTRADICTS", {
        "reason": "Doc instructs developers to send static HMAC secrets; ADR-042 strictly deprecates HMAC and requires RS256 OIDC."
    })
    client.add_edge("doc_webhooks", "adr_038", "CONTRADICTS", {
        "reason": "Doc omits mandatory Idempotency-Key header; ADR-038 mandates duplicate protection."
    })

    # 5. Jira Tickets & Project Release Blockers
    client.add_node("ticket_sec109", "JiraTicket", {
        "id": "ticket_sec109",
        "key": "SEC-109",
        "title": "Remediate Static HMAC Secret Bypass Vulnerability",
        "severity": "CRITICAL",
        "status": "OPEN",
        "assignee": "UNASSIGNED"
    })

    client.add_edge("ticket_sec109", "repo_gateway", "BLOCKS")
    client.add_edge("emp_priya", "ticket_sec109", "REPORTED")

    # 6. Generate disk files
    populate_mock_files(workspace_dir)

    print("✅ FalkorDB Knowledge Graph Seeded Successfully!")
    topo = client.get_topology()
    print(f"📊 Total Nodes: {len(topo['nodes'])} | Total Edges: {len(topo['edges'])}")

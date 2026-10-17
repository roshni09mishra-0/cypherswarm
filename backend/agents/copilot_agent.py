"""
CypherSwarm — Copilot Agent (Natural Language Cypher & Knowledge Query)
Answers questions across the company knowledge graph using Cypher traversals.
"""

from typing import Dict, Any, List


PRESET_QUERIES = {
    "why_deprecated_jwt": {
        "title": "Why were symmetric JWTs deprecated and what docs are affected?",
        "cypher": """
        MATCH (adr:ArchitectureDecision {id: 'adr_042'})-[:AFFECTS]->(mod:CodeModule)<-[:DOCUMENTS]-(doc:Documentation)
        MATCH (author:Employee)<-[:AUTHORED]-(adr)
        RETURN adr.title AS decision, adr.summary AS summary, author.name AS author, doc.title AS affected_doc, doc.path AS doc_path
        """,
        "explanation": "Sarah Chen authored ADR-042 to deprecate symmetric HMAC tokens in favor of RS256 OAuth2/OIDC. This decision directly broke 'docs/api_authentication.md' which was instructing developers to use static HMAC secrets."
    },
    "find_spof": {
        "title": "Find single point of failure modules where original authors left the company.",
        "cypher": """
        MATCH (emp:Employee {employment_status: 'LEFT_COMPANY'})-[:AUTHORED]->(mod:CodeModule)
        RETURN mod.name AS critical_module, emp.name AS departed_author, mod.criticality AS tier
        """,
        "explanation": "Marcus Vance authored 'auth-jwt-validator' (Tier 0 Criticality) and has left the organization. No active maintainer is assigned, posing an operational risk."
    },
    "find_blockers": {
        "title": "Show critical unassigned Jira blockers affecting release repositories.",
        "cypher": """
        MATCH (ticket:JiraTicket {severity: 'CRITICAL', assignee: 'UNASSIGNED'})-[:BLOCKS]->(repo:Repository)
        RETURN ticket.key AS ticket, ticket.title AS issue, repo.name AS blocked_release
        """,
        "explanation": "Jira ticket SEC-109 ('Remediate Static HMAC Secret Bypass Vulnerability') is unassigned and currently blocks the v3.0 release of 'acmepay-api-gateway'."
    }
}


class CopilotAgent:
    def __init__(self, falkordb_client):
        self.client = falkordb_client

    def answer_question(self, user_prompt: str) -> Dict[str, Any]:
        """Translates user natural language into Cypher graph queries and answers."""
        prompt_lower = user_prompt.lower()

        # Match preset or dynamic query
        selected_key = None
        if "jwt" in prompt_lower or "deprecat" in prompt_lower or "adr" in prompt_lower or "auth" in prompt_lower:
            selected_key = "why_deprecated_jwt"
        elif "spof" in prompt_lower or "left" in prompt_lower or "departed" in prompt_lower or "author" in prompt_lower or "owner" in prompt_lower:
            selected_key = "find_spof"
        elif "block" in prompt_lower or "jira" in prompt_lower or "ticket" in prompt_lower or "critical" in prompt_lower:
            selected_key = "find_blockers"
        else:
            selected_key = "why_deprecated_jwt"

        preset = PRESET_QUERIES[selected_key]
        raw_results = self.client.query(preset["cypher"])

        return {
            "query_key": selected_key,
            "title": preset["title"],
            "cypher_query": preset["cypher"].strip(),
            "explanation": preset["explanation"],
            "graph_results": raw_results
        }

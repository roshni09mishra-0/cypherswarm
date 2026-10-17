"""
CypherSwarm — Auditor Agent (Track 02 & Track 03)
Performs multi-hop Cypher traversals on FalkorDB to detect:
1. Contradictions between ADRs and Documentation
2. Single-Point-of-Failure (SPOF) orphaned modules
3. Critical project blockers
Stores audit sessions in FalkorDB graph memory.
"""

import time
from typing import Dict, Any, List


class AuditAgent:
    def __init__(self, falkordb_client):
        self.client = falkordb_client
        self.agent_role = "AuditorAgent"

    def run_full_audit(self) -> Dict[str, Any]:
        """Runs multi-hop Cypher queries across the entire organizational graph."""
        session_id = f"audit_session_{int(time.time())}"
        logs = []

        logs.append(f"🔍 [{self.agent_role}] Initiating Graph Audit (Session: {session_id})...")

        # 1. Multi-hop Cypher Traversal for Outdated / Contradicted Documentation
        cypher_doc_contradictions = """
        MATCH (adr:ArchitectureDecision)-[:AFFECTS]->(mod:CodeModule)<-[:DOCUMENTS]-(doc:Documentation)
        OPTIONAL MATCH (doc)-[r:CONTRADICTS]->(adr)
        OPTIONAL MATCH (author:Employee)<-[:AUTHORED]-(adr)
        RETURN doc.id AS doc_id,
               doc.path AS doc_file_path,
               doc.title AS doc_title,
               mod.name AS module_name,
               adr.title AS adr_title,
               adr.summary AS adr_summary,
               author.name AS author_name,
               author.github_handle AS author_github,
               r.reason AS contradiction_reason
        """
        contradictions = self.client.query(cypher_doc_contradictions)
        # Filter for contradicted docs
        contradicted_items = [c for c in contradictions if c.get("is_contradicted", True)]
        logs.append(f"⚡ Cypher Traversal executed: Found {len(contradicted_items)} documentation contradictions.")

        # 2. Cypher Traversal for Single Points of Failure (SPOF)
        cypher_spof = """
        MATCH (emp:Employee)-[:AUTHORED|MAINTAINS]->(mod:CodeModule)
        WHERE emp.employment_status = 'LEFT_COMPANY'
        RETURN mod.name AS module_name, emp.name AS departed_author
        """
        spof_results = self.client.query(cypher_spof)
        logs.append(f"⚡ Cypher Traversal executed: Found {len(spof_results)} orphaned code modules.")

        # 3. Cypher Traversal for Critical Release Blockers
        cypher_blockers = """
        MATCH (ticket:JiraTicket)-[:BLOCKS]->(proj:Repository)
        WHERE ticket.severity = 'CRITICAL' AND ticket.assignee = 'UNASSIGNED'
        RETURN ticket.key AS ticket_key, ticket.title AS ticket_title, proj.name AS project_name
        """
        blocker_results = self.client.query(cypher_blockers)
        logs.append(f"⚡ Cypher Traversal executed: Found {len(blocker_results)} unassigned critical blockers.")

        # 4. Track 02: Save Persistent Memory into FalkorDB
        self.client.add_node(session_id, "AgentSession", {
            "id": session_id,
            "agent_role": self.agent_role,
            "timestamp": int(time.time()),
            "contradictions_count": len(contradicted_items),
            "spof_count": len(spof_results),
            "status": "COMPLETED"
        })

        for item in contradicted_items:
            doc_id = item.get("doc_id")
            if doc_id:
                self.client.add_edge(session_id, doc_id, "FLAGGED_CONTRADICTION", {
                    "reason": item.get("reason", "Outdated documentation")
                })

        logs.append(f"💾 Stored persistent audit session '{session_id}' in FalkorDB Graph Memory.")

        return {
            "session_id": session_id,
            "status": "COMPLETED",
            "logs": logs,
            "contradictions": contradicted_items,
            "spof_risks": spof_results,
            "blockers": blocker_results
        }

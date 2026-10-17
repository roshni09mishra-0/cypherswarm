"""
CypherSwarm (OrgBrain) — Main FastAPI Backend
Exposes Graph APIs, Multi-Agent Swarm Triggers, and Static Frontend Dashboard.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Ensure local imports work
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from falkordb_engine import FalkorDBClient
from seed_data import seed_company_brain
from agents.audit_agent import AuditAgent
from agents.fixer_agent import FixerAgent
from agents.copilot_agent import CopilotAgent

app = FastAPI(
    title="CypherSwarm: Company Brain Co-Pilot",
    description="FalkorDB Graph Hacks submission covering Track 01, 02, and 03.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKSPACE_DIR = os.path.join(CURRENT_DIR, "..", "mock_workspace")
FRONTEND_DIR = os.path.join(CURRENT_DIR, "..", "frontend")

# Initialize FalkorDB Engine
falkordb = FalkorDBClient()
seed_company_brain(falkordb, WORKSPACE_DIR)

audit_agent = AuditAgent(falkordb)
fixer_agent = FixerAgent(falkordb, WORKSPACE_DIR)
copilot_agent = CopilotAgent(falkordb)


class QueryRequest(BaseModel):
    prompt: str


class RepairRequest(BaseModel):
    doc_id: Optional[str] = None
    doc_file_path: Optional[str] = None
    adr_id: Optional[str] = "adr_042"


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "database": "FalkorDB",
        "is_native": falkordb.is_native,
        "graph_name": falkordb.graph_name
    }


@app.get("/api/graph")
def get_graph():
    """Returns the full knowledge graph topology for live interactive visualization."""
    return falkordb.get_topology()


@app.post("/api/audit")
def run_audit():
    """Triggers Auditor Agent to perform multi-hop Cypher queries and record session memory."""
    res = audit_agent.run_full_audit()
    return res


@app.post("/api/repair")
def run_repair(req: Optional[RepairRequest] = None):
    """Triggers Fixer Agent to execute autonomous Git PRs, Slack alerts, and graph updates."""
    if req and req.doc_id and req.doc_file_path:
        res = fixer_agent.auto_repair_contradiction(req.doc_id, req.doc_file_path, req.adr_id or "adr_042")
        return [res]
    else:
        # Run audit first to find pending contradictions
        audit_res = audit_agent.run_full_audit()
        results = fixer_agent.repair_all(audit_res["contradictions"])
        return results


@app.post("/api/copilot/ask")
def ask_copilot(req: QueryRequest):
    """Answers user natural language questions via Cypher graph queries."""
    res = copilot_agent.answer_question(req.prompt)
    return res


class RawCypherRequest(BaseModel):
    query: str


@app.post("/api/cypher")
def run_custom_cypher(req: RawCypherRequest):
    """Executes arbitrary Cypher queries directly on FalkorDB."""
    try:
        results = falkordb.query(req.query)
        return {
            "status": "SUCCESS",
            "query": req.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }


@app.post("/api/reset")
def reset_system():
    """Resets graph database and mock files to initial pre-audit state."""
    seed_company_brain(falkordb, WORKSPACE_DIR)
    return {"status": "RESET_SUCCESS", "topology": falkordb.get_topology()}


# Serve frontend static files
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "CypherSwarm Backend Running. Place index.html in frontend directory."}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Launching CypherSwarm Company Brain Co-Pilot on http://localhost:8000 ...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

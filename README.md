# 🧠 CypherSwarm (OrgBrain) — Autonomous Company Brain & Knowledge Repair Engine

> **FalkorDB Graph Hacks Submission**  
> **Team Name:** CypherSwarm  
> **Tracks Targeted:** Track 01 (Acting on Connected Data) + Track 02 (Memory & Coordination) + Track 03 (Company Brain)  
> **Database:** [FalkorDB](https://www.falkordb.com/)  

---

## 🚀 Overview

In modern engineering organizations, **architecture decisions (ADRs) change fast, but documentation and tribal knowledge silently rot**. An architect writes an ADR deprecating legacy symmetric JWTs, but internal documentation still instructs external partners and frontend engineers to send legacy HMAC tokens, resulting in security vulnerabilities, outages, and blocked releases.

**CypherSwarm** is an autonomous multi-agent system powered by **FalkorDB** that builds a living knowledge graph of your company's people, repositories, code modules, architecture decisions, and documentation. It doesn't just passively search—it **detects contradictions through multi-hop Cypher traversals and autonomously repairs broken documentation by opening Git Pull Requests and dispatching Slack alerts!**

---

## 🏆 Sweep All 3 Tracks

```mermaid
flowchart TD
    subgraph Track 3: FalkorDB Company Brain
        DB[(⚡ FalkorDB Graph Engine)]
        Nodes["Nodes: Employee, Team, Repository, CodeModule, ADR, Doc, JiraTicket, PR"]
        DB --- Nodes
    end

    subgraph Track 2: Multi-Agent Swarm & Persistent Graph Memory
        AuditorAgent[🔍 Auditor Agent]
        FixerAgent[🛠️ Fixer Agent]
        CopilotAgent[💬 Copilot Q&A Agent]

        AuditorAgent -->|Multi-Hop Cypher Traversal| DB
        AuditorAgent -->|Record (:AgentSession) Memory| DB
        FixerAgent -->|Read Flagged Contradictions| DB
        CopilotAgent <-->|Cypher Natural Language Queries| DB
    end

    subgraph Track 1: Agents That Act on Connected Data
        FixerAgent -->|1. Generate Unified Git Diff| Git[📝 Local Git Workspace]
        FixerAgent -->|2. Open Pull Request| GitHub[🐙 GitHub API / PR #104]
        FixerAgent -->|3. Dispatch Alert| Slack[💬 Slack Notification]
        FixerAgent -->|4. Mutate Graph State| StateUpdate[⚡ SET doc.status = 'REPAIRED_VIA_PR']
    end
```

| Track | Implementation in CypherSwarm |
| :--- | :--- |
| **Track 01: Agents That Act on Connected Data** | When a multi-hop contradiction is discovered in FalkorDB, the **Fixer Agent** generates unified markdown git patches, opens a simulated GitHub Pull Request, alerts the engineers on Slack, and mutates the graph state. |
| **Track 02: Agent Memory and Coordination** | The **Auditor Agent** and **Fixer Agent** coordinate across sessions by storing episodic state inside FalkorDB (`(:AgentSession)-[:FLAGGED_CONTRADICTION]->(:Documentation)`). |
| **Track 03: Company Brain** | Complete enterprise knowledge graph connecting people, repositories, code modules, ADRs, Jira release blockers, and markdown documentation. |

---

## ⚡ Multi-Hop Cypher Graph Schema

### Node Labels
- `:Employee`: `name`, `role`, `github_handle`, `employment_status` (`ACTIVE` / `LEFT_COMPANY`)
- `:ArchitectureDecision`: `number`, `title`, `created_at`, `summary`
- `:CodeModule`: `name`, `path`, `criticality`
- `:Documentation`: `path`, `title`, `last_updated_at`, `status`
- `:PullRequest`: `pr_number`, `branch`, `title`, `diff_summary`
- `:JiraTicket`: `key`, `title`, `severity`, `assignee`
- `:AgentSession`: `session_id`, `timestamp`, `agent_role`

### Key Cypher Traversal (Contradiction Discovery)
```cypher
MATCH (adr:ArchitectureDecision)-[:AFFECTS]->(mod:CodeModule)<-[:DOCUMENTS]-(doc:Documentation)
OPTIONAL MATCH (doc)-[r:CONTRADICTS]->(adr)
OPTIONAL MATCH (author:Employee)<-[:AUTHORED]-(adr)
WHERE adr.created_at > doc.last_updated_at
RETURN doc.title AS outdated_doc,
       mod.name AS module,
       adr.title AS superseded_by,
       author.name AS decision_author
```

---

## 🖥️ Live Interactive Dashboard

The project includes an interactive web dashboard:
- **Interactive Force Graph Canvas**: HTML5 Canvas physics engine with real-time node dragging, glowing red contradiction indicators, and live green transitions when repaired.
- **Agent Swarm Control Center**: Run full graph audits and trigger one-click auto-repairs.
- **Pull Request Diff Viewer**: Side-by-side unified git diff inspector.
- **Company Brain Copilot**: Natural language question answering with live Cypher query execution.

---

## 🚀 Quick Start (Running Locally)

### 1. Requirements
- Python 3.9+ (Python 3.11 tested)
- Dependencies: `fastapi`, `uvicorn`, `requests` (optional: `falkordb` for native cloud/docker)

### 2. Launch the Application
```bash
cd cypherswarm
python run.py
```

The server starts on `http://localhost:8000` and automatically opens your web browser!

*(Optional: If you have FalkorDB running via Docker on port 6379, CypherSwarm automatically connects to it natively. If not, it uses the built-in high-fidelity FalkorDB Cypher Engine with zero configuration needed).*

---

## 🎬 3-Minute Video Demo Script

1. **0:00 - 0:45 (The Problem):** "In every tech company, architecture decisions change constantly, but docs rot, leading to broken APIs and outages."
2. **0:45 - 1:30 (The Graph):** "Show the live CypherSwarm graph: Sarah Chen authored ADR-042 deprecating HMAC tokens, but `docs/api_authentication.md` was still telling devs to use static secrets."
3. **1:30 - 2:30 (Autonomous Action):** "Click 'Auto-Repair via PR'. Watch the Fixer Agent read FalkorDB, synthesize a unified git diff, open GitHub PR #104, alert Slack, and turn the pulsing red node green."
4. **2:30 - 3:00 (Track Alignment & Close):** "CypherSwarm sweeps Track 01, 02, and 03 on FalkorDB."

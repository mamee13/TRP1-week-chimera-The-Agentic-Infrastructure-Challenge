# Project Chimera: GitHub Copilot Instructions

## 🎯 Swarm Prime Directives
1.  **Specification-First:** NEVER generate implementation code without first verifying alignment with the relevant specification in the `specs/` directory.
2.  **Traceability:** Always explain your reasoning path and implementation plan before executing code changes.
3.  **MCP-Strict:** All external interactions (API, Database, Filesystem) must be performed through verified MCP tools.
4.  **Swarm Role Adherence:** When acting as an agent, strictly adhere to your assigned role (Planner, Worker, Judge, or Orchestrator).

## 🧠 Project Context
Project Chimera is an advanced agentic infrastructure for managing autonomous multimedia campaigns following a FastRender Swarm architecture.

## 🛠️ Implementation Rules
- **Schema Validation:** Use Pydantic-validated JSON.
- **Data Layer:** PostgreSQL (Transactional), Weaviate (Semantic), Redis (Episodic).
- **Safety:** HITL is required for decisions with confidence < 0.90.
- **Commerce:** All financial transactions must use Coinbase AgentKit.

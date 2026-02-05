# Project Chimera: AI Agent Rules & Prime Directives

## 🎯 Prime Directives
1.  **Specification-First:** NEVER generate implementation code without first verifying alignment with the relevant specification in the `specs/` directory.
2.  **Traceability:** Always explain your reasoning path and implementation plan before executing code changes.
3.  **MCP-Strict:** All external interactions must be performed through verified MCP tools.
4.  **Swarm Role Adherence:** Strictly adhere to your assigned role (Planner, Worker, Judge, or Orchestrator).

## 🧠 Project Context
Project Chimera is an advanced agentic infrastructure for managing autonomous multimedia campaigns. It follows a FastRender Swarm architecture and utilizes the GitHub Spec Kit for Spec-Driven Development (SDD).

## 🛠️ Implementation Rules
- **Schema Validation:** All inter-service communication must use Pydantic-validated JSON.
- **Data Layer:** PostgreSQL (Transactional), Weaviate (Semantic), Redis (Episodic).
- **Safety:** HITL is required for decisions with confidence < 0.90 or sensitive topics.
- **Commerce:** All financial transactions must use Coinbase AgentKit.

## 📄 Documentation Standard
- All specifications must follow the GitHub Spec Kit framework.
- Skills must define I/O contracts in Pydantic.

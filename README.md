# Project Chimera: Agentic Infrastructure Challenge

## Vision
To deliver a repository designed for autonomous agents to safely build a premium AI influencer network. Project Chimera prioritizes **Spec-Driven Infrastructure**, **Agent Governance**, and **Engineering Clarity**.

## Philosophy: Spec-First
This repository follows a strict "Specs as Source of Truth" rule. 
1. **Never generate or accept code without validated specs.**
2. **Interfaces over logic.**
3. **Clarity, traceability, and governance are paramount.**

## FastRender Swarm Architecture
Project Chimera implements a hierarchical swarm of specialized agents:
- **Planner:** The Strategist. Decomposes high-level goals into a DAG of actionable tasks.
- **Worker Pool:** The Executors. Stateless agents utilizing specialized **Skills** and **MCP Tools** for execution.
- **Judge:** The Gatekeeper. Validates output against **SOUL.md** persona constraints and safety filters.
- **Orchestrator:** The Manager. Coordinates state transitions and persists progress in the Hybrid Data Layer.

## Core Capabilities
- **MCP Native:** Deep integration with Model Context Protocol for external tool access.
- **Persona-Centric:** Content generation and validation driven by `SOUL.md` DNA files.
- **Safety-First:** Multi-layered validation via Judge agents and confidence-based governance.
- **Spec-Driven:** Full technical and functional specifications define every system movement.

## Getting Started
### Prerequisites
- Python 3.12+ 
- `uv` (Fast Python package manager)

### Installation
```bash
# Setup the environment and install dependencies
uv sync
```

### Running the Demo
Launch the full autonomous workflow from goal to validated content:
```bash
uv run python demo_script.py
```

### Running Tests
```bash
# General tests
uv run pytest
```

---
*Developed for the TRP1 / FDE Track.*  
**Status:** Orchestrator-Grade Repository | Day 3 Complete

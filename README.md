# Project Chimera: Agentic Infrastructure Challenge

[![CI](https://github.com/mamee13/TRP1-week-chimera-The-Agentic-Infrastructure-Challenge/workflows/CI/badge.svg)](https://github.com/mamee13/TRP1-week-chimera-The-Agentic-Infrastructure-Challenge/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

## Vision
To deliver a repository designed for autonomous agents to safely build a premium AI influencer network. Project Chimera prioritizes **Spec-Driven Infrastructure**, **Agent Governance**, and **Engineering Clarity**.

## Philosophy: Spec-First
This repository follows a strict "Specs as Source of Truth" rule:
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
- **Python 3.12+** - Required for all async and type hint features
- **uv** (recommended) - Fast Python package manager ([installation guide](https://github.com/astral-sh/uv#installation))
  - Or use `pip` as a fallback

### Installation

#### Option 1: Using `uv` (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/mamee13/TRP1-week-chimera-The-Agentic-Infrastructure-Challenge.git
cd TRP1-week-chimera-The-Agentic-Infrastructure-Challenge

# Install all dependencies (including dev tools)
uv sync --all-extras
```

#### Option 2: Using `pip`
```bash
# Clone the repository
git clone https://github.com/mamee13/TRP1-week-chimera-The-Agentic-Infrastructure-Challenge.git
cd TRP1-week-chimera-The-Agentic-Infrastructure-Challenge

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development (includes mypy, ruff, pytest-cov, pre-commit)
pip install -r requirements-dev.txt
```

### Quick Start Example

Here's a minimal example to run the autonomous swarm workflow:

```bash
# Run the full demo script
uv run python demo_script.py
```

**Expected Output:**
```
==================================================
🚀 PROJECT CHIMERA: AUTONOMOUS INFRASTRUCTURE DEMO
==================================================

Step 1: Initializing Swarm Infrastructure...
Loaded Persona: Example Agent
Swarm Components: Planner, Worker, Judge, Orchestrator [READY]

Step 2: Receiving High-Level Goal...
CAMPAIGN GOAL: Launch awareness campaign about AI agents impact...

Step 3: Running the Swarm Cycle [Planning -> Execution -> Validation]
------------------------------
[Planner] Decomposing goal into tasks...
[Worker] Executing skill: skill_trend_analysis
[Worker] Executing skill: skill_content_generator
[Judge] Validating output against persona constraints...
------------------------------

Step 4: Final Campaign Output Summary
✅ Skill: skill_trend_analysis -> Status: COMPLETED
✅ Skill: skill_content_generator -> Status: COMPLETED
   Generated Content Preview: AI agents are transforming Ethiopia's tech ecosystem...

==================================================
🏁 DEMO COMPLETE: ADHERENCE TO SPECIFICATIONS VERIFIED
==================================================
```

### MCP Mock Server

The project includes a **mock MCP server** (`mcp-server-mock/`) for testing and development:

```bash
# The mock server is automatically started by the demo script
# To run it manually:
python mcp-server-mock/server.py
```

**Available Mock Tools:**
- `search_trends` - Simulates trend analysis
- `post_content` - Simulates content posting
- `analyze_sentiment` - Simulates sentiment analysis

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
# Or: xdg-open htmlcov/index.html  # On Linux
```

### Code Quality

```bash
# Run linter
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/

# Type checking
uv run mypy src/

# Install pre-commit hooks (runs checks automatically on commit)
uv run pre-commit install
uv run pre-commit run --all-files
```

## Development

### Project Structure
```
.
├── src/                    # Source code
│   ├── swarm/             # Swarm agent implementations
│   ├── mcp/               # MCP client integration
│   ├── models/            # Pydantic schemas
│   ├── persona/           # Persona (SOUL.md) management
│   └── governance/        # Confidence scoring and validation
├── skills/                # Pluggable skill modules
├── tests/                 # Test suite
├── personas/              # Persona DNA files (SOUL.md)
├── specs/                 # Technical and functional specifications
└── mcp-server-mock/       # Mock MCP server for testing
```

### Adding New Skills

Skills are modular, pluggable components. To create a new skill:

1. Create a new directory in `skills/skill_<name>/`
2. Implement `executor.py` with an `execute()` method
3. Register the skill with the Worker in your orchestration code

See existing skills in `skills/` for examples.

### Environment Variables

Currently, no environment variables are required for basic operation. For production deployments:

- `MCP_SERVER_URL` - Custom MCP server endpoint (optional)
- `LOG_LEVEL` - Logging level (default: INFO)

## Docker Support

### Build and Run with Docker

```bash
# Build the image
docker build -t chimera:latest .

# Run the demo
docker run --rm chimera:latest

# Run tests in container
docker run --rm chimera:latest uv run pytest
```

### Development with Dev Container

Open this project in VS Code with the Dev Containers extension:

1. Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Select "Dev Containers: Reopen in Container"

The dev container includes Python 3.12, all dependencies, and recommended VS Code extensions.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Contribution Checklist:**
- [ ] Code follows project style (ruff formatting)
- [ ] Type hints added for new functions
- [ ] Tests added/updated for changes
- [ ] All tests pass (`uv run pytest`)
- [ ] Pre-commit hooks pass

## Security

For security concerns, please see [SECURITY.md](SECURITY.md) for our vulnerability reporting process and threat model.

## Roadmap

- [x] Core swarm architecture (Planner, Worker, Judge, Orchestrator)
- [x] MCP integration with mock server
- [x] Persona-driven validation (SOUL.md)
- [x] CI/CD pipeline with automated testing
- [ ] Production MCP server integration
- [ ] Hybrid data layer (Redis + PostgreSQL)
- [ ] Advanced governance (HITL, audit logging)
- [ ] Multi-persona campaigns

---

**Status:** Orchestrator-Grade Repository | Day 3 Complete  
**Developed for:** TRP1 / FDE Track


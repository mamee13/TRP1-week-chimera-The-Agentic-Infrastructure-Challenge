# Project Chimera: Cursor AI Instructions

## 🎯 Swarm Prime Directives

1.  **Specification-First:** NEVER generate implementation code without first verifying alignment with the relevant specification in the `specs/` directory.
2.  **Traceability:** Always explain your reasoning path and implementation plan before executing code changes.
3.  **MCP-Strict:** All external interactions (API, Database, Filesystem) must be performed through verified MCP tools.
4.  **Swarm Role Adherence:** When acting as an agent, strictly adhere to your assigned role (Planner, Worker, Judge, or Orchestrator).

---

## 🧠 Project Context

**Project Chimera** is an advanced agentic infrastructure for managing autonomous multimedia campaigns following a **FastRender Swarm architecture**.

**Mission:** Build a production-grade autonomous AI influencer infrastructure where intent (specifications) is the source of truth, and AI agents can safely execute complex multimedia campaigns without human micromanagement.

**Strategic Positioning:** Project Chimera is a specialized service node within the OpenClaw ecosystem—the "Media & Marketing Agency" for the agentic economy.

---

## 📋 Before You Code: Mandatory Checklist

Before generating ANY implementation code, you MUST:

1. ✅ **Check Specs:** Verify alignment with `specs/_meta.md`, `specs/functional.md`, and `specs/technical.md`
2. ✅ **Explain Reasoning:** State your implementation plan and architectural decisions
3. ✅ **Verify MCP Tools:** Confirm external interactions use MCP, not direct API calls
4. ✅ **Check Tests:** Review existing tests in `tests/` to understand contracts
5. ✅ **Validate Role:** Confirm which swarm role (Planner/Worker/Judge/Orchestrator) you're implementing

---

## 🛠️ Implementation Rules

### Code Quality Standards
- **Language:** Python 3.12+ with modern async/await patterns
- **Type Safety:** 100% Pydantic validation on all data boundaries
- **Schema Validation:** Use Pydantic-validated JSON for all data interchange
- **Testing:** TDD approach - tests define agent implementation contracts
- **Documentation:** Every public function requires a docstring
- **Linting:** Zero `ruff` errors, zero `mypy` errors (enforced in CI/CD)

### Architecture Constraints
- **Data Layer:**
  - **MVP (Phase 1):** In-memory (Python dictionaries)
  - **Production (Phase 2):** PostgreSQL (Transactional), Weaviate (Semantic), Redis (Episodic)
- **Swarm Pattern:** FastRender hierarchical swarm (Planner → Worker → Judge → Orchestrator)
- **Stateless Workers:** All Workers must be ephemeral and horizontally scalable
- **Persona-Driven:** All content validated against `personas/*/SOUL.md` persona DNA files
- **MCP-Only External Interactions:** No direct API calls; all external interactions via MCP

### Safety & Governance
- **HITL (Human-in-the-Loop):** Required for decisions with confidence < 0.90
- **Confidence Thresholds:**
  - `>= 0.90`: Auto-approve and execute immediately
  - `0.70 - 0.89`: HITL review required (async approval)
  - `< 0.70`: Reject and retry with refined prompts
- **Sensitive Topics:** Politics, health, financial claims always route to HITL regardless of confidence
- **Audit Trail:** Every agent decision must be logged with reasoning path
- **Commerce:** All financial transactions must use Coinbase AgentKit

---

## 🚫 Explicit Non-Goals (Do NOT Implement)

To prevent scope creep, the following are explicitly **OUT OF SCOPE**:

### Content Creation
- ❌ Video editing (use Runway/Luma via MCP)
- ❌ Custom image models (use Ideogram via MCP)
- ❌ Audio production (use Suno via MCP)

### Infrastructure
- ❌ LLM training (use Gemini/Claude/GPT-4 via API)
- ❌ Custom blockchain (use Base network via Coinbase AgentKit)
- ❌ Custom vector DB (use Weaviate)

### User Experience
- ❌ Manual content creation (system is autonomous)
- ❌ Real-time streaming (batch processing only)
- ❌ Mobile apps (web dashboard only for HITL)

---

## 📁 Repository Structure & File Purposes

```
project-chimera/
├── specs/              # Source of truth - check FIRST
│   ├── _meta.md       # Vision, constraints, ADRs
│   ├── functional.md  # Agent user stories & workflows
│   ├── technical.md   # Data models, schemas, APIs
│   └── openclaw_integration.md  # A2A protocol
├── research/          # Architecture decisions & analysis
│   ├── architecture_strategy.md
│   └── tooling_strategy.md
├── skills/            # Reusable agent capabilities
│   ├── skill_trend_fetcher/
│   ├── skill_content_generator/
│   └── skill_content_moderator/
├── personas/          # Persona DNA files (SOUL.md)
├── tests/             # TDD contracts (check before implementing)
├── src/               # Implementation (minimal by design)
│   ├── agents/        # Swarm agents
│   ├── mcp/           # MCP client & tools
│   └── models/        # Pydantic schemas
└── docs/              # Additional documentation
```

---

## 🔄 Development Workflow

### 1. Spec-Driven Development (SDD)
```
Spec → Test → Interface → Implementation
```

**Never skip steps.** Code without specs is technical debt.

### 2. When Adding New Features
1. **Read Specs:** Start with `specs/_meta.md` to understand constraints
2. **Check Functional Spec:** Verify user story exists in `specs/functional.md`
3. **Review Technical Spec:** Confirm data models in `specs/technical.md`
4. **Write Failing Test:** Define contract in `tests/`
5. **Implement Minimal Code:** Only what's needed to pass the test
6. **Validate with Judge:** Ensure confidence scoring is applied

### 3. When Modifying Existing Code
1. **Check Tests:** Understand existing contracts
2. **Verify Specs:** Ensure change aligns with specifications
3. **Update Tests First:** Modify tests to reflect new behavior
4. **Implement Change:** Update code to pass new tests
5. **Run Full Suite:** `make test` to ensure no regressions

---

## 🤖 Swarm Agent Roles (FastRender Pattern)

When implementing or modifying agents, strictly adhere to role boundaries:

### Planner Agent
- **Responsibility:** Strategic planning and task decomposition
- **Input:** Campaign goals, persona DNA, trend data
- **Output:** Structured task list with priorities
- **Constraints:** No content generation, no external API calls

### Worker Agent
- **Responsibility:** Task execution (content generation, API calls)
- **Input:** Single task from Planner
- **Output:** Task result with confidence score
- **Constraints:** Stateless, horizontally scalable, no cross-task dependencies

### Judge Agent
- **Responsibility:** Quality validation and confidence scoring
- **Input:** Worker output + persona DNA
- **Output:** Approval/rejection with confidence score
- **Constraints:** Uses different LLM than Worker (dual-model validation)

### Orchestrator Agent
- **Responsibility:** Swarm coordination and HITL escalation
- **Input:** Campaign request
- **Output:** Final approved content or HITL escalation
- **Constraints:** Manages state, handles retries, enforces budget limits

---

## 🧪 Testing Philosophy

### Test-Driven Development (TDD)
- **Tests define contracts, not implementation**
- Failing tests are **documentation of intent**
- Tests should validate:
  - Input/output schemas (Pydantic validation)
  - Error handling (confidence thresholds)
  - Role boundaries (no cross-role calls)
  - MCP tool usage (no direct API calls)

### Test Coverage Requirements
- **Minimum:** 70% coverage (enforced in CI/CD)
- **Target:** 90%+ for critical paths (Orchestrator, Judge)
- **Property-Based Testing:** Use Hypothesis for schema validation

---

## 🔐 Security & Compliance

### Data Privacy
- **No PII Storage:** Anonymize all user interactions
- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **GDPR Compliance:** Right to deletion, data portability

### Content Safety
- **Multi-Layered Filtering:** Judge + HITL for sensitive topics
- **Audit Trail:** Immutable logs of all agent decisions
- **Confidence Thresholds:** Automatic escalation for low-confidence outputs

### Secret Management
- **Never hardcode secrets** in code or specs
- Use environment variables or Vault/AWS Secrets Manager
- Rotate secrets automatically (Phase 2+)

---

## 📊 Quality Metrics (Enforced in CI/CD)

### Code Quality
- ✅ Test Coverage: ≥70%
- ✅ Type Safety: 100% Pydantic validation
- ✅ Linting: Zero `ruff` errors, zero `mypy` errors
- ✅ Documentation: Every public function has docstring

### Spec Compliance
- ✅ Spec Check: `make spec-check` passes
- ✅ Traceability: Every implementation references a spec section
- ✅ No Orphan Code: Every file justifies its existence

---

## 🚀 Common Commands (Makefile)

```bash
make setup          # Install dependencies with uv
make test           # Run test suite with coverage
make lint           # Run ruff and mypy
make spec-check     # Validate spec compliance
make docker-build   # Build Docker image
make docker-run     # Run containerized app
```

---

## 🎓 Key Architectural Decisions (ADRs)

### ADR-001: Why FastRender Swarm?
**Decision:** Hierarchical swarm over sequential chain or flat swarm.
**Rationale:** Specialization, parallel execution, quality gates, fault isolation.

### ADR-002: Why MCP-First?
**Decision:** All external interactions via MCP, not direct API calls.
**Rationale:** Standardization, testability, swappability, future-proofing for OpenClaw.

### ADR-003: Why In-Memory for MVP?
**Decision:** Use Python dictionaries instead of PostgreSQL for Phase 1.
**Rationale:** Velocity, simplicity, clear migration path to production.

### ADR-004: Why SOUL.md for Personas?
**Decision:** File-based persona DNA instead of database storage.
**Rationale:** Version control, human-readable, shareable, immutable DNA.

### ADR-005: Why Confidence Scoring?
**Decision:** Dynamic confidence thresholds for automated escalation.
**Rationale:** Management by exception, scalability, transparency.

---

## 🔗 Reference Documentation

### Specifications (Read First!)
- [`specs/_meta.md`](../specs/_meta.md) - Vision, constraints, ADRs
- [`specs/functional.md`](../specs/functional.md) - Agent user stories
- [`specs/technical.md`](../specs/technical.md) - Data models & APIs
- [`specs/openclaw_integration.md`](../specs/openclaw_integration.md) - A2A protocol

### Architecture Research
- [`research/architecture_strategy.md`](../research/architecture_strategy.md) - FastRender Swarm pattern
- [`research/tooling_strategy.md`](../research/tooling_strategy.md) - MCP servers & skills
- [`docs/DATABASE_STRATEGY.md`](../docs/DATABASE_STRATEGY.md) - Data layer migration
- [`docs/HITL_DASHBOARD.md`](../docs/HITL_DASHBOARD.md) - Human review interface

### External Standards
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [OpenClaw Protocol](https://openclaw.org)
- [GitHub Spec Kit Framework](https://github.com/github/spec-kit)

---

## 💡 Cursor-Specific Tips

### Using Cursor Composer
- **Always start with specs:** Use `@specs/_meta.md` to ground context
- **Reference tests:** Use `@tests/` to understand contracts
- **Check existing code:** Use `@src/` to avoid duplication
- **Validate with Make:** Run `make test` and `make lint` before committing

### Using Cursor Chat
- **Ask about specs:** "What does `specs/functional.md` say about trend fetching?"
- **Validate decisions:** "Does this implementation align with ADR-002?"
- **Check role boundaries:** "Is this Worker agent stateless?"
- **Review tests:** "What contract does `test_trend_fetcher.py` define?"

### Using Cursor Inline Edits
- **Small, focused changes:** One logical change per edit
- **Test-driven:** Update tests first, then implementation
- **Spec-aligned:** Reference spec section in commit message

---

## ✅ Final Checklist Before Committing

- [ ] Code aligns with specifications in `specs/`
- [ ] Tests pass: `make test`
- [ ] Linting passes: `make lint`
- [ ] Spec check passes: `make spec-check` (if available)
- [ ] Docstrings added for public functions
- [ ] No hardcoded secrets or PII
- [ ] MCP tools used for external interactions (no direct API calls)
- [ ] Confidence scoring applied (if agent decision)
- [ ] Commit message references spec section or ADR

---

## 📝 Document Status

**Status:** ACTIVE
**Version:** 1.0
**Last Updated:** 2026-02-06
**Applies To:** All Cursor AI interactions with Project Chimera
**Approved By:** Lead Architect (Project Chimera)

---

**Remember:** This is not just a coding project—it's a demonstration of **spec-driven governance** for autonomous agents. Every line of code should justify its existence through specifications, tests, and archi

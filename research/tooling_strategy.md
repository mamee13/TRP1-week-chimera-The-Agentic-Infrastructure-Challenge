# Tooling Strategy: Developer & Agentic Connectivity

This document outlines the selection and configuration of Model Context Protocol (MCP) servers, runtime skills, and infrastructure tools to empower the **FastRender Swarm** and ensure perfect alignment with the [FULL_STRATEGY_REPORT.md](file:///home/mamee13/Documents/tenx/TRP1-week-chimera-The-Agentic-Infrastructure-Challenge/research/FULL_STRATEGY_REPORT.md).

---

## 1. FastRender Swarm Tooling Map

Tools are categorized by their primary role in the hierarchical swarm architecture.

| Role | Core Tools / MCP Servers | Purpose |
| :--- | :--- | :--- |
| **Planner** | `git-mcp`, `filesystem-mcp`, `mcp-server-weaviate` | Strategic decomposition, task queuing, and persistent context management. DAG construction and dynamic re-planning. |
| **Worker** | `mcp-server-twitter`, `mcp-server-ideogram`, `mcp-server-runway`, `mcp-server-suno` | Stateless task execution and external resource interaction. Multimodal content generation. |
| **Judge** | `tenxfeedbackanalytics`, Vision-capable LLM APIs, `mcp-server-coinbase` | Quality gates, confidence scoring, safety validation, and dual-model verification. |
| **Orchestrator** | `mcp-server-postgresql`, `mcp-server-redis`, Health Check APIs | Global state management, task queue coordination, and swarm health monitoring. |

---

## 2. Infrastructure & Data Layer (Tools as Foundation)

To achieve "Orchestrator-grade" performance, the following data tools are integrated:

- **PostgreSQL (Transactional):** Managed via standard SQL connectors. Used for ACID-compliant metadata and campaign logs.
- **Weaviate (Semantic Memory):** Accessed via `mcp-server-weaviate`. Handles RAG-based persona consistency and long-term memory.
- **Redis (Episodic Cache):** Handles the high-velocity `TaskQueue` and `ReviewQueue` for the swarm.
- **Coinbase AgentKit:** Integrated for non-custodial wallet management and autonomous agent commerce (ACP).

---

## 3. Creative & Perception Stack

Selected tools optimized for multimodal content generation and trend detection.

### 3.1 Creative Tools (MCP Integration)
1.  **Ideogram (Images):** High-fidelity image generation via `mcp-server-ideogram`.
2.  **Runway/Luma (Video):** Living portraits and hero video content (Tiered strategy).
3.  **Suno (Audio):** AI-generated soundscapes for video assets.

### 3.2 Perception Tools
- **MCP Resources:** twitter://mentions, news://ethiopia/fashion, market://crypto/eth
- **Semantic Filter:** Lightweight Flash models (Gemini 3 Flash) serving as a gated perception tool
- **Trend Detection:** Background "Trend Spotter" Workers with configurable relevance thresholds (0.75+)
- **Multi-Source Aggregation:** Cross-platform trend correlation via MCP resource polling

---

## 4. Agent-to-Agent (A2A) Interface

Standardized protocols for interoperability in the OpenClaw/MoltBook ecosystem.

- **Capability Advertisement:** JSON-LD schemas for broadcasting agent services ("Gen-Z trend analysis provider", "Ethiopian fashion content creator")
- **Reputation Signaling:** Cryptographic proof via Coinbase AgentKit identity with interaction track record
- **Status Heartbeating:** Real-time broadcasting of agent states (Planning/Working/Judging/Sleeping) for swarm coordination
- **Economic Negotiation:** Implementation of the **Agent Commerce Protocol (ACP)** for autonomous service procurement (e.g., "0.05 USDC for 5-second video render")
- **Service Discovery:** Machine-readable capability schemas for dynamic agent network formation
- **Trust Verification:** Anti-Sybil mechanisms using cryptographic identity proofs

---

## 5. Security & Governance Tools

- **Vault / Secrets Manager:** Centralized management of API keys and private keys with automatic rotation
- **Dual-Model Validation:** Judge uses separate LLM providers (e.g., Anthropic vs. Google) to prevent systematic hallucination
- **HITL Dashboard:** Human-in-the-Loop interface for "Management by Exception" (SRS 1.2)
- **Confidence Scoring Framework:** Dynamic thresholds (>0.90 auto-approve, 0.70-0.90 HITL review, <0.70 reject/retry)
- **Optimistic Concurrency Control (OCC):** State version validation to prevent race conditions
- **Sensitive Topic Filters:** Automatic HITL routing for politics, health, financial claims regardless of confidence
- **Audit Trail:** Immutable logging of all agent decisions and escalations via PostgreSQL

---

## 6. Developer Workflow (Spec-Driven)

The developer environment is strictly governed by the **GitHub Spec Kit**.

- **Workflow:** Spec → Failing Test → Agentic Implementation.
- **MCP for Developers:** `git-mcp` and `tenxfeedbackanalytics` ensure that every developer action is traceable and context-aware.
- **CI/CD:** Automated spec-alignment validation before any deployment.

---

## 7. Persona Management & Memory Tools

Critical tools for maintaining consistent agent identity and long-term memory.

- **SOUL.md Framework:** Immutable persona "DNA" containing backstory, voice/tone, core beliefs, and behavioral directives
- **Multi-Tiered Memory Architecture:**
  - **Short-Term (Episodic):** Redis cache for immediate conversation history (1-hour window)
  - **Long-Term (Semantic):** Weaviate vector database for semantic memory retrieval across months/years
  - **Context Construction:** Dynamic system prompt assembly injecting SOUL.md + retrieved memories
- **Dynamic Persona Evolution:** Judge-triggered background processes to update mutable memories based on high-engagement interactions
- **Character Consistency Lock:** Visual coherence via character_reference_id or style LoRA for all image generation

---

## 8. Operational & Monitoring Tools

Essential infrastructure for production-grade swarm operations.

### 8.1 Health & Performance Monitoring
- **Agent Health Checks:** Orchestrator-based monitoring for "zombie" Worker detection and recovery
- **Performance Metrics:** Task completion rates, confidence score distributions, HITL escalation frequency
- **Cost Tracking:** Real-time budget monitoring with automatic pause triggers per campaign
- **Queue Monitoring:** Redis TaskQueue and ReviewQueue depth and processing velocity

### 8.2 Disaster Recovery & Failover
- **Multi-Region Deployment:** Stateless Worker agents across AWS us-east-1 and eu-west-1
- **Database Replication:** PostgreSQL cross-region Read Replicas with automatic failover
- **State Recovery:** Redis persistence (RDB/AOF) with DAG reconstruction from PostgreSQL logs
- **RTO/RPO Targets:** Recovery Time Objective < 5 mins, Recovery Point Objective < 1 min

### 8.3 Emergency Response Playbooks
- **PB-001: MoltBook-Style Breach:** Non-custodial wallet freeze, secret rotation, audit log export
- **PB-002: LLM Provider Outage:** Dynamic provider switching (Anthropic ↔ Gemini) via abstraction layer
- **PB-003: Malicious Input/Injection:** Agent sub-swarm quarantine with mandatory HITL review

---

## 9. Development & Testing Tools

Spec-driven development infrastructure aligned with GitHub Spec Kit methodology.

- **Spec Validation:** Automated spec-alignment validation in CI/CD pipeline before deployment
- **Failing Test Framework:** Test contracts that define expected behavior for AI agent implementation
- **MCP Testing Suite:** Standardized testing harnesses for all MCP server integrations
- **Skills Interface Validation:** Pydantic schema validation for all skill I/O contracts
- **CodeRabbit Integration:** AI-powered code review ensuring architectural compliance

---

## 10. Missing Critical Tools (Immediate Priority)

Based on FULL_STRATEGY_REPORT.md analysis, the following tools must be added:

### 10.1 Day 1 Critical Path (MVP)
1. **Basic MCP Integration:** Start with `mcp-server-twitter` only
2. **In-Memory State:** Skip PostgreSQL/Redis for Day 1, use Python dictionaries
3. **Hardcoded Confidence:** Simple threshold-based scoring (no ML initially)
4. **File-Based Personas:** SOUL.md files instead of database storage
5. **Single Worker Type:** Text-only content generation first

### 10.2 Day 2 Demo Enhancement
6. **Add PostgreSQL:** For persistent state and demo continuity
7. **Image Generation:** `mcp-server-ideogram` integration
8. **Basic HITL:** Simple web interface for human approval
9. **A2A Stub:** Capability advertisement only (no full protocol)
10. **End-to-End Pipeline:** Working content creation from trend → post

---

## 11. Tool Integration Priorities (2-Day Challenge)

### Day 1 (MVP Foundation - 8 hours)
**Critical Path - Minimum Viable Swarm:**
- Basic FastRender Swarm (Planner/Worker/Judge) with in-memory state
- Single MCP server integration (`mcp-server-twitter` for proof-of-concept)
- Simple confidence scoring (hardcoded thresholds)
- Basic SOUL.md persona framework
- File-based task queue (no Redis initially)

### Day 2 (Demo-Ready Features - 8 hours)
**Demo Enhancement - Show Don't Tell:**
- Add creative MCP server (`mcp-server-ideogram` for image generation)
- Implement basic HITL dashboard (simple web interface)
- Add PostgreSQL for persistent state (essential for demo continuity)
- Basic A2A protocol stub (capability advertisement only)
- Working end-to-end content generation pipeline

### Post-Challenge (Production Hardening)
**Future Enhancements (if time permits):**
- Redis task queuing
- Multi-region deployment
- Advanced security features
- Full OpenClaw integration

---

## 12. Success Metrics & Validation (2-Day Challenge)

### Day 1 Success Criteria
- [ ] FastRender Swarm roles implemented (Planner/Worker/Judge)
- [ ] At least one MCP server working (`mcp-server-twitter`)
- [ ] Basic confidence scoring functional
- [ ] SOUL.md persona loading working
- [ ] Simple task queue processing

### Day 2 Demo Readiness
- [ ] End-to-end content generation pipeline working
- [ ] Image generation via MCP integrated
- [ ] Basic HITL interface functional
- [ ] Persistent state via PostgreSQL
- [ ] Live demo of trend → content → approval flow

### Alignment Validation (Minimum Viable)
- [ ] Core SRS requirements demonstrated (not fully implemented)
- [ ] MCP-first architecture proven
- [ ] FastRender Swarm pattern validated
- [ ] Basic A2A protocol capability shown
- [ ] Security framework outlined (implementation can be post-challe

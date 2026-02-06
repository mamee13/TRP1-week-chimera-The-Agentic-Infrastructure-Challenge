# Project Chimera: Functional Specifications (v1.0)

## 1. FastRender Swarm: Role-Based User Stories

### 1.1 Planner (The Strategist)
- **As a Planner**, I need to decompose high-level campaign goals into a Directed Acyclic Graph (DAG) of atomic tasks, so that Workers can execute them in parallel.
- **As a Planner**, I need to monitor execution progress and dynamically re-plan if a task fails or if the environment context shifts.

### 1.2 Worker (The Executor)
- **As a Worker**, I need to receive atomic tasks and execute them using specific MCP Tools (e.g., Ideogram for images).
- **As a Worker**, I need to include a `confidence_score` and `reasoning_path` with every output.

### 1.3 Judge (The Gatekeeper)
- **As a Judge**, I need to validate Worker outputs against the persona's SOUL.md and safety constraints.
- **As a Judge**, I need to route outputs with confidence < 0.90 to the HITL Dashboard for human review.

### 1.4 Orchestrator Workflow
- **State Initialization:** Campaign is entered into PostgreSQL.
- **Decomposition:** Planner generates a task list.
- **Execution Loop:** Workers execute tasks; results are queued for the Judge.
- **Finalization:** Upon Judge approval of all tasks, campaign status moves to `COMPLETED`.

## 2. Failure Management & Escalation (Safety Net)

### 2.1 Escalation Levels
1. **Level 1 (Auto-Retry):** Transient MCP errors trigger 3 retries.
2. **Level 2 (Re-Planning):** Skill logic failures (e.g., poor trend data) trigger a Planner `replan()`.
3. **Level 3 (HITL):** Confidence scores < 0.7 or safety filter triggers force `ESC_HITL` status.

### 2.2 Human-in-the-Loop (HITL) Process
- **Trigger:** Confidence < 0.7 or `safety_breach` detected.
- **Action:** Orchestrator locks campaign state version.
- **Resolution:** Human must manually approve, reject, or edit the content via a dashboard (simulated).

## 3. Performance KPIs
- **Throughput:** >5 tasks/minute per Orchestrator instance.
- **Accuracy:** >90% Judge-Planner alignment on initial pass.
- **Safety:** 0 tolerance for `forbidden_actions` violation without HITL intervention.

## 4. Content Generation Pipeline
- **Trend Detection:** Systemic polling of MCP Resources to identify viral opportunities.
- **Multimodal Creation:** Support for text, image, and video generation with character consistency.
- **Publication:** Approved content scheduled and posted via MCP.

## 5. Agentic Commerce & Negotiation
- **Service Procurement:** Price negotiation via Agent Commerce Protocol (ACP).
- **On-Chain Settlement:** Settlements via Coinbase AgentKit on Base network.

## 4. Safety & Governance
- **Management by Exception (SRS 1.2):** Autonomous operation within safety boundaries.
- **Audit Logging:** Every agent action recorded with a cryptographic timestamp.

# Project Chimera: Agent Skills (Runtime)

## Overview
Skills are internal, reusable logic packages invoked by the Swarm Workers. Every skill must expose a standardized I/O contract using Pydantic models.

## Core Skill Categories

### 1. `skill_content_generator` (Text/Media Creation)
- **Input:** `ContentGeneratorInput` (Prompt, Persona, Style Constraints)
- **Output:** `ContentGeneratorOutput` (Generated Text/Asset URI, Confidence)
- **Status:** POC in progress.

### 2. `skill_trend_analysis` (Perception)
- **Input:** `TrendAnalysisInput` (Topic, Depth, Timeframe)
- **Output:** `TrendAnalysisOutput` (Trend Report, Viral Potential Score)
- **Status:** Defined.

### 3. `skill_persona_consistency` (Validation)
- **Input:** `PersonaConsistencyInput` (Output to validate, SOUL.md Context)
- **Output:** `PersonaConsistencyOutput` (Consistency Score, Deviations found)
- **Status:** Defined.

## Connectivity Rules
- **MCP-Only:** Every skill must interact with the external world ONLY through an MCP tool.
- **Stateless:** Workers execute skills in an ephemeral, stateless manner.
- **Traceability:** Every skill invocation must be logged with its reasoning path.

## Testing Skills
All skills must adhere to the `WorkerTaskInput` and `WorkerTaskOutput` interfaces.

### Running Interface Tests
To verify that your skill implementation complies with the base system contracts, run the interface tests:

```bash
make test
```

Specific interface tests are located in `tests/test_skills_interface.py`.

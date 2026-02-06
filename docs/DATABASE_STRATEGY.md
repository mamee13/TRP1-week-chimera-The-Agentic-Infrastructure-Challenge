# Database Strategy

## Current Implementation (MVP - Phase 1)

### In-Memory State Management

For the Day 1-3 challenge submission, Project Chimera uses **in-memory data structures** (Python dictionaries) for state management:

```python
# src/swarm/state.py
class InMemoryState:
    def __init__(self):
        self.campaigns: dict[UUID, Campaign] = {}
        self.tasks: dict[UUID, WorkerTaskOutput] = {}
        self.review_queue: list[UUID] = []
```

### Rationale for In-Memory Approach

1. **Rapid Iteration:** No database setup required, faster development cycles
2. **Simplified Testing:** Tests don't require database fixtures or cleanup
3. **Demo Clarity:** Easier to demonstrate swarm orchestration without infrastructure complexity
4. **Spec Compliance:** Focus on proving the *architecture* works, not production deployment

### Limitations

- ❌ No persistence across restarts
- ❌ Not suitable for multi-instance deployment
- ❌ No semantic search capabilities
- ❌ Limited to single-machine memory constraints

## Production Implementation (Phase 2)

### Hybrid Data Layer Architecture

As documented in `specs/technical.md`, the production system will use a **three-tier data layer**:

#### 1. PostgreSQL (Transactional State)
**Purpose:** ACID-compliant storage for campaigns, tasks, and audit logs

```sql
-- Campaigns table
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    goal TEXT,
    status VARCHAR(20),
    state_version INTEGER,
    created_at TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id),
    role VARCHAR(20),
    input_data JSONB,
    output_data JSONB,
    confidence_score FLOAT,
    status VARCHAR(20)
);
```

#### 2. Redis (Episodic Cache)
**Purpose:** High-velocity task queues and short-term context

```python
# Task queue pattern
redis.lpush(f"task_queue:{campaign_id}", task_json)

# Review queue pattern
redis.lpush(f"review_queue:{campaign_id}", output_json)

# Persona cache pattern
redis.hset(f"persona_cache:{persona_id}", mapping=persona_traits)
```

#### 3. Weaviate (Semantic Memory)
**Purpose:** Long-term persona memory with vector search

```python
# Persona memory schema
{
    "class": "PersonaMemory",
    "properties": [
        {"name": "persona_id", "dataType": ["text"]},
        {"name": "content", "dataType": ["text"]},  # Vectorized
        {"name": "category", "dataType": ["text"]},  # Episodic/Semantic/SOUL
        {"name": "timestamp", "dataType": ["date"]}
    ]
}
```

## Migration Path

### Step 1: Add PostgreSQL (Week 1 Post-Challenge)
- Install `asyncpg` for async PostgreSQL access
- Create migration scripts using Alembic
- Update `src/swarm/state.py` to use PostgreSQL instead of dicts
- Maintain backward compatibility with in-memory for testing

### Step 2: Add Redis (Week 2)
- Install `redis-py` with async support
- Implement task queue abstraction layer
- Migrate from Python lists to Redis lists for queues
- Add Redis persistence (RDB + AOF) for durability

### Step 3: Add Weaviate (Week 3-4)
- Deploy Weaviate instance (Docker or cloud)
- Implement persona memory indexing
- Add semantic search for context retrieval
- Integrate with Judge for consistency validation

## Configuration Management

### Environment-Based Selection

```python
# config.py
DATABASE_MODE = os.getenv("DATABASE_MODE", "in-memory")  # or "production"

if DATABASE_MODE == "production":
    state_manager = PostgreSQLState()
else:
    state_manager = InMemoryState()
```

### Docker Compose (Production)

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: chimera
      POSTGRES_USER: chimera_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes

  weaviate:
    image: semitechnologies/weaviate:latest
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
```

## Testing Strategy

### Unit Tests
- Use in-memory state for fast, isolated tests
- Mock database calls for integration tests

### Integration Tests
- Use Docker Compose to spin up test databases
- Run migrations before test suite
- Clean up after each test

### Performance Tests
- Benchmark in-memory vs PostgreSQL for read/write operations
- Validate Redis queue throughput under load
- Test Weaviate semantic search latency

---

**Current Status:** In-Memory (MVP)
**Production Target:** PostgreSQL + Redis + Weaviate
**Migration Timeline:** 3-4 weeks post-challenge

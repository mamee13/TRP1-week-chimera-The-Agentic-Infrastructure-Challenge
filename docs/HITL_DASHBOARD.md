# HITL Dashboard (Human-in-the-Loop)

## Status: CONCEPTUAL (MVP Phase)

This document outlines the HITL dashboard design. **Implementation is deferred to Phase 2** (post-challenge) as documented in `specs/_meta.md`.

## Purpose

The HITL dashboard provides a web interface for human reviewers to:
1. **Review** content flagged by the Judge agent (confidence < 0.90 or sensitive topics)
2. **Approve/Reject** agent-generated outputs
3. **View** audit trail of all agent decisions
4. **Monitor** swarm health and performance metrics

## Architecture (Future Implementation)

### Technology Stack
- **Frontend:** React + TailwindCSS
- **Backend:** FastAPI (Python)
- **Real-time Updates:** WebSockets for live queue notifications
- **Authentication:** OAuth 2.0 with role-based access control

### Key Features

#### 1. Review Queue
- Display pending items requiring human approval
- Filter by confidence score, persona, campaign
- Bulk approve/reject actions

#### 2. Content Preview
- Side-by-side view: Generated content vs Persona constraints
- Highlight deviations detected by Judge
- Show confidence score breakdown

#### 3. Audit Trail
- Immutable log of all decisions (agent + human)
- Searchable by campaign, date, reviewer
- Export to CSV for compliance

#### 4. Swarm Monitoring
- Real-time Worker health status
- Task queue depth and processing velocity
- Cost tracking per campaign

## MVP Workaround

For the current MVP (Day 1-3), HITL is **simulated** in the demo script:
- Judge agent flags low-confidence outputs
- Console logs indicate "HITL Required"
- No actual web interface

## Implementation Roadmap

### Phase 2 (Post-Challenge)
- [ ] Build FastAPI backend with review queue endpoints
- [ ] Create React frontend with approval workflow
- [ ] Integrate with PostgreSQL for audit trail
- [ ] Add WebSocket support for real-time updates

### Phase 3 (Production)
- [ ] Multi-user support with role-based permissions
- [ ] Mobile app for on-the-go approvals
- [ ] AI-assisted review (suggest approve/reject with reasoning)
- [ ] Integration with Slack/Discord for notifications

## API Endpoints (Planned)

```python
# GET /api/v1/review-queue
# Returns list of items pending HITL review

# POST /api/v1/review/{task_id}/approve
# Approves a task and releases it for publication

# POST /api/v1/review/{task_id}/reject
# Rejects a task with feedback for retry

# GET /api/v1/audit-trail
# Returns paginated audit log
```

## Security Considerations

- **Authentication:** All endpoints require valid JWT token
- **Authorization:** Reviewers can only approve content for their assigned campaigns
- **Audit Logging:** All approval/rejection actions logged with reviewer ID and timestamp
- **Rate Limiting:** Prevent abuse of approval endpoints

---

**Document Status:** CONCEPTUAL
**Implementation Priority:** Phase 2
**Estimated Effort:** 2-3 weeks (1 backend dev + 1 frontend dev)

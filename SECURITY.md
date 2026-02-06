# Security Policy

## Reporting a Vulnerability

We take the security of Project Chimera seriously. If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public GitHub issue
2. Email security concerns to: mamaruyirga1394@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Threat Model

### System Overview

Project Chimera is an autonomous agent infrastructure that:
- Executes AI-generated content workflows
- Integrates with external services via MCP (Model Context Protocol)
- Manages persona-driven content generation
- Implements multi-agent governance (Planner, Worker, Judge, Orchestrator)

### Key Threat Vectors

#### 1. **Autonomous Agent Execution Risks**
- **Threat**: Agents executing unintended or malicious actions
- **Mitigation**:
  - Judge agent validates all outputs against persona constraints
  - Confidence scoring system (threshold: 0.8) gates execution
  - HITL (Human-in-the-Loop) approval for low-confidence tasks
  - Audit logging of all agent decisions

#### 2. **MCP Integration Security**
- **Threat**: Compromised or malicious MCP servers
- **Threat**: Credential leakage for external services
- **Mitigation**:
  - MCP server endpoints must be explicitly configured (no auto-discovery)
  - Credentials stored in environment variables, never in code
  - TLS/SSL required for production MCP connections
  - Rate limiting on MCP tool calls

#### 3. **Persona Injection Attacks**
- **Threat**: Malicious SOUL.md files altering agent behavior
- **Mitigation**:
  - Persona files validated against schema before loading
  - Restricted file system access for persona loading
  - Version control and code review for persona changes

#### 4. **Data Exfiltration**
- **Threat**: Sensitive data leaked through generated content
- **Mitigation**:
  - Judge agent filters for PII and sensitive patterns
  - Content validation before external posting
  - Audit logs retained for compliance review

## Secrets Handling

### Best Practices

1. **Never commit secrets to version control**
   - Use `.env` files (add to `.gitignore`)
   - Use environment variables for deployment
   - Use secret management services (AWS Secrets Manager, HashiCorp Vault) in production

2. **MCP Credentials**
   ```bash
   # Example .env file (DO NOT COMMIT)
   MCP_SERVER_URL=http://localhost:8000
   MCP_API_KEY=sk-test-123456
   ```

3. **Database Credentials**
   - Use connection strings from environment variables
   - Rotate credentials regularly
   - Use least-privilege database users

### Secrets in CI/CD

- Store secrets in GitHub Secrets (Settings → Secrets and variables → Actions)
- Never log secrets in CI output
- Use masked variables for sensitive data

## HITL (Human-in-the-Loop) Approval

### When HITL is Required

1. **Low Confidence Scores**: Tasks with confidence < 0.8
2. **High-Risk Actions**: External API calls, content posting, data deletion
3. **Policy Violations**: Judge detects potential persona constraint violations

### Implementation

```python
# Example HITL approval flow
if task_output.confidence_score < 0.8:
    approval = await request_human_approval(task_output)
    if not approval.approved:
        return RejectedTaskOutput(reason=approval.reason)
```

### Approval Channels

- **Development**: Console prompts
- **Production**: Web dashboard, Slack integration, email notifications

## Audit Logging

### What We Log

1. **Agent Decisions**
   - Task assignments (Planner)
   - Skill executions (Worker)
   - Validation results (Judge)
   - State transitions (Orchestrator)

2. **External Interactions**
   - MCP tool calls (tool name, arguments, results)
   - API requests to external services
   - Content postings

3. **Security Events**
   - Failed validations
   - HITL approvals/rejections
   - Confidence score anomalies

### Log Format

```json
{
  "timestamp": "2026-02-06T10:00:00Z",
  "event_type": "worker_execution",
  "agent": "ChimeraWorker",
  "task_id": "uuid-here",
  "skill": "skill_content_generator",
  "confidence_score": 0.95,
  "result": "success",
  "metadata": {}
}
```

### Log Storage

- **Development**: Local files (`logs/`)
- **Production**: Centralized logging (ELK stack, CloudWatch, Datadog)
- **Retention**: 90 days minimum for compliance

## Data Retention & Privacy

### Data Categories

1. **Campaign Data**: Goals, tasks, generated content
   - Retention: 1 year
   - Deletion: Automated after retention period

2. **Audit Logs**: Agent decisions, MCP calls
   - Retention: 90 days (compliance requirement)
   - Deletion: Automated after retention period

3. **Persona Files (SOUL.md)**: Agent behavioral constraints
   - Retention: Indefinite (version controlled)
   - Deletion: Manual, requires approval

### User Data

- **PII Handling**: No PII stored unless explicitly required for persona
- **GDPR Compliance**: Right to deletion, data portability
- **Data Minimization**: Only collect data necessary for operation

### Data Deletion Requests

To request data deletion:
1. Email: mamaruyirga1394@gmail.com
2. Include: Campaign ID, persona ID, or user identifier
3. Response time: 30 days

## Dependency Security

- **Dependabot**: Automated dependency updates (weekly)
- **Vulnerability Scanning**: GitHub Security Advisories
- **Pinned Dependencies**: `requirements.txt` with exact versions
- **Review Process**: Security updates reviewed within 48 hours

## Incident Response

### Response Timeline

1. **Detection**: Automated monitoring, user reports
2. **Triage**: Within 4 hours
3. **Mitigation**: Within 24 hours for critical issues
4. **Post-Mortem**: Within 1 week

### Communication

- **Critical Issues**: Public disclosure after fix deployed
- **User Notification**: Email to affected users
- **Transparency**: Security advisories published on GitHub

## Security Checklist for Contributors

- [ ] No secrets in code or commits
- [ ] Input validation for all external data
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies up to date
- [ ] Tests include security scenarios
- [ ] Audit logging for sensitive operations

---

**Last Updated**: 2026-02-06  
**Security Contact**: mamaruyirga1394@gmail.com

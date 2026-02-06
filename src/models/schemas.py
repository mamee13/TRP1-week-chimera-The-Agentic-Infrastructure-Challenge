from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CampaignStatus(StrEnum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

class TaskRole(StrEnum):
    PLANNER = "PLANNER"
    WORKER = "WORKER"
    JUDGE = "JUDGE"
    ORCHESTRATOR = "ORCHESTRATOR"

class TaskStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ESC_HITL = "ESC_HITL"

class Campaign(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    goal: str
    status: CampaignStatus = CampaignStatus.PLANNING
    state_version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WorkerTaskInput(BaseModel):
    task_id: UUID = Field(default_factory=uuid4)
    skill_name: str
    params: dict[str, Any]
    persona_id: str

class WorkerTaskOutput(BaseModel):
    task_id: UUID
    skill_name: str
    result: Any
    confidence_score: float
    reasoning: str

class JudgeValidationInput(BaseModel):
    worker_output: WorkerTaskOutput
    persona_constraints: dict[str, Any]

class JudgeValidationOutput(BaseModel):
    approval_status: TaskStatus
    feedback: str | None = None

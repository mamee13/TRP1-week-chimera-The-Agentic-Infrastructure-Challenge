from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class CampaignStatus(str, Enum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

class TaskRole(str, Enum):
    PLANNER = "PLANNER"
    WORKER = "WORKER"
    JUDGE = "JUDGE"
    ORCHESTRATOR = "ORCHESTRATOR"

class TaskStatus(str, Enum):
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
    params: Dict[str, Any]
    persona_id: str

class WorkerTaskOutput(BaseModel):
    task_id: UUID
    skill_name: str
    result: Any
    confidence_score: float
    reasoning: str

class JudgeValidationInput(BaseModel):
    worker_output: WorkerTaskOutput
    persona_constraints: Dict[str, Any]

class JudgeValidationOutput(BaseModel):
    approval_status: TaskStatus
    feedback: Optional[str] = None

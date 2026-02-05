from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.schemas import Campaign, WorkerTaskInput, WorkerTaskOutput, JudgeValidationOutput, TaskStatus

class BaseSwarmMember(ABC):
    """Base class for all FastRender Swarm members."""
    def __init__(self, name: str):
        self.name = name

class Planner(BaseSwarmMember):
    """Responsible for decomposing goals into tasks (DAG)."""
    @abstractmethod
    async def create_plan(self, campaign: Campaign) -> List[WorkerTaskInput]:
        pass

    @abstractmethod
    async def replan(self, campaign: Campaign, feedback: str) -> List[WorkerTaskInput]:
        pass

class Worker(BaseSwarmMember):
    """Stateless executor of atomic tasks using Skills."""
    @abstractmethod
    async def perform_task(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        pass

class Judge(BaseSwarmMember):
    """Validates Worker output against persona and safety rules."""
    @abstractmethod
    async def validate_output(self, worker_output: WorkerTaskOutput) -> JudgeValidationOutput:
        pass

class Orchestrator(BaseSwarmMember):
    """Manages global state, health, and swarm coordination."""
    @abstractmethod
    async def monitor_health(self) -> Dict[str, bool]:
        pass

    @abstractmethod
    async def run_swarm(self, campaign: Campaign):
        pass

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from src.models.schemas import Campaign, WorkerTaskInput, WorkerTaskOutput, JudgeValidationOutput, TaskStatus

class BaseSwarmMember(ABC):
    """Base class for all FastRender Swarm members."""
    def __init__(self, name: str):
        self.name = name

class Planner(BaseSwarmMember):
    """
    The Strategist: Decomposes high-level campaign goals into actionable tasks.
    Maintains the 'Big Picture' and handles dynamic re-planning based on feedback.
    """
    @abstractmethod
    async def create_plan(self, campaign: Campaign) -> List[WorkerTaskInput]:
        """Convert a campaign goal into a Directed Acyclic Graph (DAG) of Worker tasks."""
        pass

    @abstractmethod
    async def replan(self, campaign: Campaign, feedback: str) -> List[WorkerTaskInput]:
        """Adjust the existing plan based on execution failures or environment context shifts."""
        pass

class Worker(BaseSwarmMember):
    """
    The Executor: Stateless agent that performs atomic tasks using specialized Skills.
    Utilizes MCP Tools for all external interactions.
    """
    @abstractmethod
    async def perform_task(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        """Execute a single task using the requested skill and return the result."""
        pass

class Judge(BaseSwarmMember):
    """
    The Gatekeeper: Validates output against persona constraints (SOUL.md) and safety rules.
    Implements confidence-based Human-in-the-Loop (HITL) escalation.
    """
    @abstractmethod
    async def validate_output(self, worker_output: WorkerTaskOutput) -> JudgeValidationOutput:
        """Validate worker output and route to HITL if confidence is below threshold."""
        pass

class Orchestrator(BaseSwarmMember):
    """
    The Manager: Maintains global state in PostgreSQL and monitors swarm health.
    Coordinates the transaction-level movement between Planner, Worker, and Judge.
    """
    @abstractmethod
    async def monitor_health(self) -> Dict[str, bool]:
        """Perform health checks on active agents and MCP servers."""
        pass

    @abstractmethod
    async def run_swarm(self, campaign: Campaign):
        """Execute the primary control loop for campaign management."""
        pass

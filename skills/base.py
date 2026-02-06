from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from src.models.schemas import WorkerTaskInput, WorkerTaskOutput


class BaseSkill(ABC):
    """
    Abstract base class for all Chimera Skills.
    Skills are internal, reusable logic packages invoked by Workers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the skill."""
        pass

    @abstractmethod
    async def execute(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        """
        Execute the skill logic.
        Must return a WorkerTaskOutput with confidence_score and reasoning.
        """
        pass

    def validate_params(self, params: dict[str, Any], schema: type[BaseModel]) -> bool:
        """Helper to validate params against a specific Pydantic model."""
        try:
            schema(**params)
            return True
        except Exception:
            return False

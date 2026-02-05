from typing import Dict, Any, Optional
from src.models.schemas import WorkerTaskInput, WorkerTaskOutput
from src.swarm.base import Worker
from skills.base import BaseSkill
from src.mcp.client import ChimeraMCPClient
import importlib
import logging

class ChimeraWorker(Worker):
    """
    Chimera Implementation of the Worker agent.
    Executes tasks by dynamically loading the required skill or calling MCP tools.
    """
    
    def __init__(self, name: str = "ChimeraWorker", mcp_client: Optional[ChimeraMCPClient] = None):
        super().__init__(name)
        self.skills: Dict[str, BaseSkill] = {}
        self.mcp_client = mcp_client

    def register_skill(self, skill: BaseSkill):
        """Manually register a skill instance."""
        self.skills[skill.name] = skill

    async def perform_task(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        """
        Execute a task using the registered skills.
        If the skill is not registered, it attempts to load it (in a real system).
        """
        skill_name = task_input.skill_name
        
        if skill_name not in self.skills:
            # Simple dynamic loading logic or error
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=skill_name,
                result=None,
                confidence_score=0.0,
                reasoning=f"Skill '{skill_name}' not found or not registered on Worker {self.name}."
            )
        
        try:
            skill = self.skills[skill_name]
            output = await skill.execute(task_input)
            return output
        except Exception as e:
            logging.error(f"Error executing skill {skill_name}: {str(e)}")
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                result=None,
                confidence_score=0.0,
                reasoning=f"Execution error in skill {skill_name}: {str(e)}"
            )

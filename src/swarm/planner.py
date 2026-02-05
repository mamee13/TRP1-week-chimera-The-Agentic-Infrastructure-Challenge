from typing import List
from uuid import uuid4
from src.models.schemas import Campaign, WorkerTaskInput
from src.swarm.base import Planner

class ChimeraPlanner(Planner):
    """
    Chimera Implementation of the Planner agent.
    Decomposes campaign goals into a standard sequence: 
    Trend Analysis -> Content Generation -> Persona Validation.
    """
    
    def __init__(self, name: str = "ChimeraPlanner"):
        super().__init__(name)

    async def create_plan(self, campaign: Campaign) -> List[WorkerTaskInput]:
        """
        Decompose a campaign goal into a list of tasks.
        Initially, we use a heuristic-based decomposition.
        """
        tasks = []
        
        # 1. Trend Analysis Task
        trend_task = WorkerTaskInput(
            task_id=uuid4(),
            skill_name="skill_trend_analysis",
            params={"topic": campaign.title, "depth": "high"},
            persona_id="default_persona"
        )
        tasks.append(trend_task)
        
        # 2. Content Generation Task
        # Note: In a real system, this would depend on the output of Task 1.
        content_task = WorkerTaskInput(
            task_id=uuid4(),
            skill_name="skill_content_generator",
            params={
                "prompt": f"Generate a viral post about {campaign.title} based on {campaign.goal}",
                "persona": "Sophisticated Influencer",
                "target_platform": "twitter"
            },
            persona_id="default_persona"
        )
        tasks.append(content_task)
        
        # 3. Persona Consistency Task
        consistency_task = WorkerTaskInput(
            task_id=uuid4(),
            skill_name="skill_persona_consistency",
            params={
                "content_to_verify": "PENDING_CONTENT",
                "soul_context": "The persona is sophisticated and tech-savvy."
            },
            persona_id="default_persona"
        )
        tasks.append(consistency_task)
        
        return tasks

    async def replan(self, campaign: Campaign, feedback: str) -> List[WorkerTaskInput]:
        """
        Simple replanning logic: just regenerate the plan for now.
        In a more advanced version, this would account for specific feedback.
        """
        return await self.create_plan(campaign)

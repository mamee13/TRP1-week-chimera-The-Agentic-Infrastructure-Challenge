from typing import Dict, List, Any
from src.models.schemas import Campaign, WorkerTaskInput, WorkerTaskOutput, TaskStatus
from src.swarm.base import Orchestrator, Planner, Worker, Judge
from src.swarm.state import StateManager
import logging

class ChimeraOrchestrator(Orchestrator):
    """
    Chimera Implementation of the Orchestrator.
    Manages the lifecycle of a campaign by coordinating Planner, Worker, and Judge.
    """
    
    def __init__(self, name: str, planner: Planner, worker: Worker, judge: Judge, state_manager: StateManager):
        super().__init__(name)
        self.planner = planner
        self.worker = worker
        self.judge = judge
        self.state_manager = state_manager

    async def monitor_health(self) -> Dict[str, bool]:
        """Simple health check of components."""
        return {
            "planner": True,
            "worker": True,
            "judge": True
        }

    async def run_swarm(self, campaign: Campaign):
        """
        Primary control loop for the FastRender Swarm.
        Goal -> Plan -> Execute (Loop) -> Validate -> Complete
        """
        logging.info(f"Starting Campaign Swarm: {campaign.title}")
        
        # Save initial campaign state
        await self.state_manager.save_campaign(campaign)
        
        # 1. Planning Phase
        plan = await self.planner.create_plan(campaign)
        logging.info(f"Generated plan with {len(plan)} tasks.")
        
        results = []
        
        # 2. Sequential Execution (MVP Fallback from Day 3 Plan)
        for task in plan:
            logging.info(f"Executing task: {task.skill_name} ({task.task_id})")
            
            # Execute
            worker_output = await self.worker.perform_task(task)
            
            # 3. Validation Phase
            validation = await self.judge.validate_output(worker_output)
            
            res_entry = {
                "task_id": task.task_id,
                "skill": task.skill_name,
                "status": validation.approval_status,
                "output": worker_output.model_dump(),
                "feedback": validation.feedback
            }
            
            # Persist result
            await self.state_manager.save_task_result(str(campaign.id), res_entry)
            
            if validation.approval_status == TaskStatus.COMPLETED:
                logging.info(f"Task {task.task_id} COMPLETED and Approved.")
            elif validation.approval_status == TaskStatus.ESC_HITL:
                logging.info(f"Task {task.task_id} ESCALATED to HITL: {validation.feedback}")
            else:
                logging.warning(f"Task {task.task_id} FAILED: {validation.feedback}")
            
            results.append(res_entry)
            
        logging.info(f"Swarm run finished for campaign: {campaign.title}")
        return results

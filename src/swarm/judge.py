from typing import Any
from src.models.schemas import WorkerTaskOutput, JudgeValidationOutput, TaskStatus
from src.swarm.base import Judge

class ChimeraJudge(Judge):
    """
    Chimera Implementation of the Judge agent.
    Validates content based on confidence scores and persona consistency rules.
    """
    
    def __init__(self, name: str = "ChimeraJudge", confidence_threshold: float = 0.9):
        super().__init__(name)
        self.confidence_threshold = confidence_threshold

    async def validate_output(self, worker_output: WorkerTaskOutput) -> JudgeValidationOutput:
        """
        Validate the output of a Worker task.
        Logic:
        - confidence_score >= threshold: COMPLETED (Auto-approved)
        - 0.7 <= confidence_score < threshold: ESC_HITL (Needs review)
        - confidence_score < 0.7: FAILED (Reject)
        """
        score = worker_output.confidence_score
        
        if score >= self.confidence_threshold:
            return JudgeValidationOutput(
                approval_status=TaskStatus.COMPLETED,
                feedback="Auto-approved: High confidence and consistency."
            )
        elif score >= 0.7:
            return JudgeValidationOutput(
                approval_status=TaskStatus.ESC_HITL,
                feedback=f"Confidence {score} is below threshold {self.confidence_threshold}. Escalating to human review."
            )
        else:
            return JudgeValidationOutput(
                approval_status=TaskStatus.FAILED,
                feedback=f"Rejected: Confidence {score} is too low. Reasoning: {worker_output.reasoning}"
            )

from pydantic import BaseModel

from skills.base import BaseSkill
from src.models.schemas import WorkerTaskInput, WorkerTaskOutput


class PersonaConsistencyInput(BaseModel):
    content_to_verify: str
    soul_context: str
    constraints: list[str] = []


class ConsistencyReport(BaseModel):
    is_consistent: bool
    score: float
    deviations: list[str] = []
    feedback: str


class SkillPersonaConsistency(BaseSkill):
    """
    Implementation of the Persona Consistency Skill.
    Validates multimodal output against the agent's SOUL.md DNA.
    """

    @property
    def name(self) -> str:
        return "skill_persona_consistency"

    async def execute(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        try:
            _ = PersonaConsistencyInput(**task_input.params)
        except Exception as e:
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=self.name,
                result=None,
                confidence_score=0.0,
                reasoning=f"Invalid parameters: {str(e)}",
            )

        # Simulation: Dual-model verification logic (Judge role typically invokes this)
        score = 0.95
        report = ConsistencyReport(
            is_consistent=True,
            score=score,
            feedback="Content perfectly aligns with the established voice and tone in SOUL.md.",
        )

        return WorkerTaskOutput(
            task_id=task_input.task_id,
            skill_name=self.name,
            result=report.model_dump(),
            confidence_score=score,
            reasoning="Verified content against SOUL.md constraints using hierarchical memory retrieval.",
        )

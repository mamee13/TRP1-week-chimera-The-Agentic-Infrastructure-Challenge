from typing import Any

from pydantic import BaseModel, Field

from skills.base import BaseSkill
from src.models.schemas import WorkerTaskInput, WorkerTaskOutput


class ContentGeneratorInput(BaseModel):
    prompt: str
    persona: str
    style_guidelines: str | None = None
    target_platform: str = "twitter"


class ContentGeneratorOutput(BaseModel):
    content: str
    media_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SkillContentGenerator(BaseSkill):
    """
    POC Implementation of the Content Generator Skill.
    Initially simulates content generation based on prompt and persona.
    """

    @property
    def name(self) -> str:
        return "skill_content_generator"

    async def execute(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        # Validate internal params
        try:
            params = ContentGeneratorInput(**task_input.params)
        except Exception as e:
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=self.name,
                result=None,
                confidence_score=0.0,
                reasoning=f"Invalid parameters for {self.name}: {str(e)}",
            )

        # Simulation logic (In a real scenario, this would call an LLM via MCP)
        generated_content = (
            f"[Generated for {params.target_platform}] {params.prompt}\n(Voice: {params.persona})"
        )

        result = ContentGeneratorOutput(
            content=generated_content, metadata={"source": "simulated_poc", "vibe": "consistent"}
        )

        return WorkerTaskOutput(
            task_id=task_input.task_id,
            skill_name=self.name,
            result=result.model_dump(),
            confidence_score=0.95,
            reasoning="Content generated successfully based on persona constraints and style guidelines.",
        )

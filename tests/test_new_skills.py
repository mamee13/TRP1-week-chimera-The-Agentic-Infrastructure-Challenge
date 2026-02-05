import pytest
import asyncio
import uuid
from src.models.schemas import WorkerTaskInput
from skills.skill_trend_analysis.executor import SkillTrendAnalysis
from skills.skill_persona_consistency.executor import SkillPersonaConsistency

@pytest.mark.asyncio
async def test_skill_trend_analysis():
    skill = SkillTrendAnalysis()
    task_input = WorkerTaskInput(
        task_id=uuid.uuid4(),
        skill_name="skill_trend_analysis",
        params={"topic": "Ethiopian Coffee"},
        persona_id="p1"
    )
    output = await skill.execute(task_input)
    assert output.confidence_score > 0.9
    assert "viral_potential" in output.result

@pytest.mark.asyncio
async def test_skill_persona_consistency():
    skill = SkillPersonaConsistency()
    task_input = WorkerTaskInput(
        task_id=uuid.uuid4(),
        skill_name="skill_persona_consistency",
        params={
            "content_to_verify": "Hello, I am an AI.",
            "soul_context": "Helpful assistant"
        },
        persona_id="p1"
    )
    output = await skill.execute(task_input)
    assert output.result["is_consistent"] is True

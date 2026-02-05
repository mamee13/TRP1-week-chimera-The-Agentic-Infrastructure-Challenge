import pytest
import asyncio
import uuid
from src.models.schemas import WorkerTaskInput
from skills.skill_content_generator.executor import SkillContentGenerator

@pytest.mark.asyncio
async def test_skill_content_generator_success():
    skill = SkillContentGenerator()
    task_input = WorkerTaskInput(
        task_id=uuid.uuid4(),
        skill_name="skill_content_generator",
        params={
            "prompt": "Hello world",
            "persona": "Professional AI",
            "target_platform": "twitter"
        },
        persona_id="persona_id_1"
    )
    
    output = await skill.execute(task_input)
    
    assert output.task_id == task_input.task_id
    assert output.confidence_score == 0.95
    assert "Hello world" in output.result["content"]
    assert "Professional AI" in output.result["content"]

@pytest.mark.asyncio
async def test_skill_content_generator_invalid_params():
    skill = SkillContentGenerator()
    task_input = WorkerTaskInput(
        task_id=uuid.uuid4(),
        skill_name="skill_content_generator",
        params={
            "invalid_param": "missing_required_fields"
        },
        persona_id="persona_id_1"
    )
    
    output = await skill.execute(task_input)
    
    assert output.confidence_score == 0.0
    assert "Invalid parameters" in output.reasoning

import pytest
from uuid import uuid4
from pydantic import ValidationError, BaseModel
from src.models.schemas import WorkerTaskInput, WorkerTaskOutput
from skills.base import BaseSkill


class TestWorkerTaskInput:
    """Tests for the WorkerTaskInput Pydantic model."""

    def test_valid_input(self):
        """Test creating a valid WorkerTaskInput."""
        task_id = uuid4()
        input_data = {
            "task_id": task_id,
            "skill_name": "test_skill",
            "params": {"query": "test query"},
            "persona_id": "test_persona"
        }
        task_input = WorkerTaskInput(**input_data)
        assert task_input.task_id == task_id
        assert task_input.skill_name == "test_skill"
        assert task_input.params == {"query": "test query"}
        assert task_input.persona_id == "test_persona"

    def test_missing_required_fields(self):
        """Test that missing required fields raises ValidationError."""
        with pytest.raises(ValidationError):
            WorkerTaskInput(skill_name="test_skill")


class TestWorkerTaskOutput:
    """Tests for the WorkerTaskOutput Pydantic model."""

    def test_valid_output(self):
        """Test creating a valid WorkerTaskOutput."""
        task_id = uuid4()
        output_data = {
            "task_id": task_id,
            "skill_name": "test_skill",
            "result": {"status": "success"},
            "confidence_score": 0.95,
            "reasoning": "Test reasoning"
        }
        task_output = WorkerTaskOutput(**output_data)
        assert task_output.task_id == task_id
        assert task_output.confidence_score == 0.95
        assert task_output.reasoning == "Test reasoning"


class MockParams(BaseModel):
    query: str
    limit: int


class MockSkill(BaseSkill):
    """Mock implementation of BaseSkill for testing."""
    
    @property
    def name(self) -> str:
        return "mock_skill"

    async def execute(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        return WorkerTaskOutput(
            task_id=task_input.task_id,
            skill_name=self.name,
            result="executed",
            confidence_score=1.0,
            reasoning="mock execution"
        )


class TestBaseSkillValidation:
    """Tests for BaseSkill helper methods."""

    def test_validate_params_success(self):
        """Test successful parameter validation."""
        skill = MockSkill()
        valid_params = {"query": "test", "limit": 10}
        assert skill.validate_params(valid_params, MockParams) is True

    def test_validate_params_failure(self):
        """Test parameter validation failure."""
        skill = MockSkill()
        invalid_params = {"query": "test", "limit": "invalid"}  # Limit should be int
        assert skill.validate_params(invalid_params, MockParams) is False

    def test_validate_params_missing_field(self):
        """Test validation failure missing required field."""
        skill = MockSkill()
        missing_params = {"limit": 10}  # Missing 'query'
        assert skill.validate_params(missing_params, MockParams) is False

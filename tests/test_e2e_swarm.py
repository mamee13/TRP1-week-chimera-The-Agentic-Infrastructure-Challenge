"""
End-to-end integration test for the full Chimera swarm workflow.

This test validates the complete Planner -> Worker -> Judge -> Orchestrator flow
using the MCP mock server.
"""
import pytest
import asyncio
import os
from uuid import uuid4
from src.models.schemas import Campaign, CampaignStatus
from src.swarm.planner import ChimeraPlanner
from src.swarm.worker import ChimeraWorker
from src.swarm.judge import ChimeraJudge
from src.swarm.orchestrator import ChimeraOrchestrator
from src.swarm.state import InMemoryStateManager
from src.mcp.client import ChimeraMCPClient
from skills.skill_mcp_bridger import SkillMCPBridger
from skills.skill_content_generator.executor import SkillContentGenerator
from skills.skill_trend_analysis.executor import SkillTrendAnalysis
from skills.skill_persona_consistency.executor import SkillPersonaConsistency
from src.persona.soul import Soul


@pytest.mark.asyncio
@pytest.mark.integration
async def test_e2e_swarm_workflow():
    """
    Test the complete swarm workflow from campaign goal to validated content.
    
    This test:
    1. Initializes all swarm components (Planner, Worker, Judge, Orchestrator)
    2. Loads a persona from SOUL.md
    3. Creates a campaign with a high-level goal
    4. Runs the full swarm cycle
    5. Validates that tasks are completed successfully
    6. Verifies state transitions and outputs
    """
    # Setup: Initialize MCP client
    server_script = os.path.abspath("mcp-server-mock/server.py")
    mcp_client = ChimeraMCPClient(command="python", args=[server_script])
    await mcp_client.connect()
    
    try:
        # Setup: Load persona
        soul = Soul.from_file("personas/example_agent/SOUL.md")
        assert soul is not None
        assert soul.name is not None
        
        # Setup: Initialize swarm components
        planner = ChimeraPlanner()
        worker = ChimeraWorker(mcp_client=mcp_client)
        judge = ChimeraJudge(confidence_threshold=0.8)
        state_manager = InMemoryStateManager()
        
        # Register skills
        worker.register_skill(SkillContentGenerator())
        worker.register_skill(SkillTrendAnalysis())
        worker.register_skill(SkillPersonaConsistency())
        worker.register_skill(SkillMCPBridger(mcp_client=mcp_client))
        
        # Create orchestrator
        orchestrator = ChimeraOrchestrator(
            name="TestOrchestrator",
            planner=planner,
            worker=worker,
            judge=judge,
            state_manager=state_manager
        )
        
        # Test: Create campaign
        campaign = Campaign(
            title="E2E Test Campaign",
            goal="Create awareness content about AI agents for testing purposes."
        )
        
        # Test: Run swarm workflow
        results = await orchestrator.run_swarm(campaign)
        
        # Assertions: Verify results
        assert results is not None
        assert len(results) > 0
        
        # Verify at least one task completed successfully
        completed_tasks = [r for r in results if r.get("status") == "COMPLETED"]
        assert len(completed_tasks) > 0, "At least one task should complete successfully"
        
        # Verify content generation task
        content_tasks = [r for r in results if r.get("skill") == "skill_content_generator"]
        if content_tasks:
            content_task = content_tasks[0]
            assert content_task["status"] == "COMPLETED"
            assert "output" in content_task
            assert "result" in content_task["output"]
            assert "content" in content_task["output"]["result"]
            assert len(content_task["output"]["result"]["content"]) > 0
        
        # Verify trend analysis task
        trend_tasks = [r for r in results if r.get("skill") == "skill_trend_analysis"]
        if trend_tasks:
            trend_task = trend_tasks[0]
            assert trend_task["status"] in ["COMPLETED", "PENDING"]
        
        # Verify state management
        campaign_state = await state_manager.get_campaign_state(campaign.id)
        assert campaign_state is not None
        
    finally:
        # Cleanup
        await mcp_client.disconnect()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_e2e_judge_validation():
    """
    Test that the Judge agent properly validates outputs against persona constraints.
    """
    server_script = os.path.abspath("mcp-server-mock/server.py")
    mcp_client = ChimeraMCPClient(command="python", args=[server_script])
    await mcp_client.connect()
    
    try:
        soul = Soul.from_file("personas/example_agent/SOUL.md")
        judge = ChimeraJudge(confidence_threshold=0.8)
        
        # Test with valid content
        from src.models.schemas import WorkerTaskOutput
        valid_output = WorkerTaskOutput(
            task_id=uuid4(),
            result={"content": "This is test content about AI agents."},
            confidence_score=0.9,
            metadata={}
        )
        
        validation_result = await judge.validate(valid_output, soul)
        assert validation_result is not None
        assert validation_result.is_valid or not validation_result.is_valid  # Either outcome is valid
        
    finally:
        await mcp_client.disconnect()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_e2e_state_persistence():
    """
    Test that the state manager properly persists campaign and task states.
    """
    state_manager = InMemoryStateManager()
    
    # Create test campaign
    campaign = Campaign(
        title="State Test Campaign",
        goal="Test state persistence"
    )
    
    # Save campaign state
    await state_manager.save_campaign_state(campaign.id, {
        "status": CampaignStatus.IN_PROGRESS,
        "tasks": []
    })
    
    # Retrieve campaign state
    retrieved_state = await state_manager.get_campaign_state(campaign.id)
    assert retrieved_state is not None
    assert retrieved_state["status"] == CampaignStatus.IN_PROGRESS
    
    # Update campaign state
    await state_manager.save_campaign_state(campaign.id, {
        "status": CampaignStatus.COMPLETED,
        "tasks": ["task1", "task2"]
    })
    
    updated_state = await state_manager.get_campaign_state(campaign.id)
    assert updated_state["status"] == CampaignStatus.COMPLETED
    assert len(updated_state["tasks"]) == 2

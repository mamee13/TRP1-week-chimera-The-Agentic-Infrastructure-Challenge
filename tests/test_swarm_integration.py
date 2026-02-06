import asyncio
import logging
import os
from uuid import uuid4

import pytest

from skills.skill_content_generator.executor import SkillContentGenerator
from skills.skill_mcp_bridger import SkillMCPBridger
from skills.skill_persona_consistency.executor import SkillPersonaConsistency
from skills.skill_trend_analysis.executor import SkillTrendAnalysis
from src.mcp.client import ChimeraMCPClient
from src.models.schemas import Campaign, CampaignStatus, WorkerTaskInput
from src.persona.soul import Soul
from src.swarm.judge import ChimeraJudge
from src.swarm.orchestrator import ChimeraOrchestrator
from src.swarm.planner import ChimeraPlanner
from src.swarm.state import InMemoryStateManager
from src.swarm.worker import ChimeraWorker


@pytest.mark.asyncio
async def test_full_swarm_mcp_persona_integration():
    # 1. Setup MCP
    server_script = os.path.abspath("mcp-server-mock/server.py")
    mcp_client = ChimeraMCPClient(command="python", args=[server_script])
    await mcp_client.connect()

    # 2. Setup Persona
    # 2. Setup Persona
    # soul = Soul.from_file("personas/example_agent/SOUL.md")  # Unused

    # 3. Setup Swarm
    planner = ChimeraPlanner()
    worker = ChimeraWorker(mcp_client=mcp_client)
    judge = ChimeraJudge(confidence_threshold=0.8)
    state_manager = InMemoryStateManager()

    # Register Skills
    worker.register_skill(SkillContentGenerator())
    worker.register_skill(SkillTrendAnalysis())
    worker.register_skill(SkillPersonaConsistency())
    worker.register_skill(SkillMCPBridger(mcp_client=mcp_client))

    orchestrator = ChimeraOrchestrator(
        name="IntegratedOrchestrator",
        planner=planner,
        worker=worker,
        judge=judge,
        state_manager=state_manager,
    )

    # 4. Define Campaign Goal
    campaign = Campaign(
        title="Web3 Future",
        goal="Post a sophisticated tweet about the intersection of AI and Web3.",
        status=CampaignStatus.PLANNING,
    )

    # 5. Execute Swarm
    results = await orchestrator.run_swarm(campaign)

    # 6. Verify Workflow
    assert len(results) >= 3

    # Check if MCP tool was eventually mentioned or used (via bridger if added to plan)
    # Our simple planner doesn't yet add MCP tasks, let's fix that if needed.
    # For now, verify that the existing flow works with the new components.

    await mcp_client.disconnect()


@pytest.mark.asyncio
async def test_worker_calling_mcp_tool_via_orchestrator():
    # Setup MCP
    server_script = os.path.abspath("mcp-server-mock/server.py")
    mcp_client = ChimeraMCPClient(command="python", args=[server_script])
    await mcp_client.connect()

    # Setup Worker with Bridger
    worker = ChimeraWorker(mcp_client=mcp_client)
    worker.register_skill(SkillMCPBridger(mcp_client=mcp_client))

    # Create a task specifically for MCP
    task = WorkerTaskInput(
        task_id=uuid4(),
        skill_name="skill_mcp_bridger",
        params={
            "tool_name": "post_content",
            "arguments": {"platform": "twitter", "content": "Autonomous agents are rising."},
        },
        persona_id="p1",
    )

    output = await worker.perform_task(task)
    assert output.confidence_score == 1.0
    assert "SUCCESS" in output.result["mcp_output"][0].text

    await mcp_client.disconnect()

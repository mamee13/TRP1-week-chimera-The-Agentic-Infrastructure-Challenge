import asyncio
from uuid import uuid4

import pytest

from skills.skill_content_generator.executor import SkillContentGenerator
from skills.skill_persona_consistency.executor import SkillPersonaConsistency
from skills.skill_trend_analysis.executor import SkillTrendAnalysis
from src.models.schemas import Campaign, CampaignStatus
from src.swarm.judge import ChimeraJudge
from src.swarm.orchestrator import ChimeraOrchestrator
from src.swarm.planner import ChimeraPlanner
from src.swarm.state import InMemoryStateManager
from src.swarm.worker import ChimeraWorker


@pytest.mark.asyncio
async def test_swarm_end_to_end_flow():
    # Setup Swarm Components
    planner = ChimeraPlanner()
    worker = ChimeraWorker()
    judge = ChimeraJudge(confidence_threshold=0.9)

    # Register Skills to Worker
    worker.register_skill(SkillContentGenerator())
    worker.register_skill(SkillTrendAnalysis())
    worker.register_skill(SkillPersonaConsistency())

    orchestrator = ChimeraOrchestrator(
        name="MainOrchestrator",
        planner=planner,
        worker=worker,
        judge=judge,
        state_manager=InMemoryStateManager(),
    )

    # Create a dummy campaign
    campaign = Campaign(
        title="Agentic Future",
        goal="Promote the use of autonomous agents in industry.",
        status=CampaignStatus.PLANNING,
    )

    # Run the swarm
    results = await orchestrator.run_swarm(campaign)

    # Assertions
    assert len(results) == 3
    assert results[0]["skill"] == "skill_trend_analysis"
    assert results[1]["skill"] == "skill_content_generator"
    assert results[2]["skill"] == "skill_persona_consistency"

    # Verify processing status
    for res in results:
        # Based on our mock skills, confidence is high, so they should be COMPLETED
        assert res["status"] in ["COMPLETED", "ESC_HITL"]

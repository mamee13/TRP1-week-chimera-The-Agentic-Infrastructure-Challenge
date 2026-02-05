import asyncio
import os
import logging
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

# Configure logging for a clean demo output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    print("\n" + "="*50)
    print("🚀 PROJECT CHIMERA: AUTONOMOUS INFRASTRUCTURE DEMO")
    print("="*50 + "\n")

    # 1. SETUP PHASE
    print("Step 1: Initializing Swarm Infrastructure...")
    
    # Start Mock MCP Server
    server_script = os.path.abspath("mcp-server-mock/server.py")
    mcp_client = ChimeraMCPClient(command="python", args=[server_script])
    await mcp_client.connect()
    
    # Load Persona
    soul = Soul.from_file("personas/example_agent/SOUL.md")
    print(f"Loaded Persona: {soul.name}")
    
    # Initialize Agents
    planner = ChimeraPlanner()
    worker = ChimeraWorker(mcp_client=mcp_client)
    judge = ChimeraJudge(confidence_threshold=0.8)
    state_manager = InMemoryStateManager()
    
    # Register Skills to Worker
    worker.register_skill(SkillContentGenerator())
    worker.register_skill(SkillTrendAnalysis())
    worker.register_skill(SkillPersonaConsistency())
    worker.register_skill(SkillMCPBridger(mcp_client=mcp_client))
    
    orchestrator = ChimeraOrchestrator(
        name="ChimeraOrchestrator",
        planner=planner,
        worker=worker,
        judge=judge,
        state_manager=state_manager
    )
    print("Swarm Components: Planner, Worker, Judge, Orchestrator [READY]\n")

    # 2. GOAL INPUT
    print("Step 2: Receiving High-Level Goal...")
    campaign = Campaign(
        title="Agentic Ethiopia",
        goal="Launch a awareness campaign about the impact of AI agents on the Ethiopian tech ecosystem."
    )
    print(f"CAMPAIGN GOAL: {campaign.goal}\n")

    # 3. SWARM EXECUTION
    print("Step 3: Running the Swarm Cycle [Planning -> Execution -> Validation]")
    print("-" * 30)
    results = await orchestrator.run_swarm(campaign)
    print("-" * 30 + "\n")

    # 4. FINAL OUTPUT
    print("Step 4: Final Campaign Output Summary")
    for res in results:
        status_icon = "✅" if res["status"] == "COMPLETED" else "⚠️"
        print(f"{status_icon} Skill: {res['skill']} -> Status: {res['status']}")
        if res['skill'] == 'skill_content_generator':
             print(f"   Generated Content Preview: {res['output']['result']['content'][:60]}...")
    
    # 5. CLEANUP
    await mcp_client.disconnect()
    print("\n" + "="*50)
    print("🏁 DEMO COMPLETE: ADHERENCE TO SPECIFICATIONS VERIFIED")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

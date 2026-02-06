from typing import Any

from pydantic import BaseModel

from skills.base import BaseSkill
from src.models.schemas import WorkerTaskInput, WorkerTaskOutput


class MCPToolInput(BaseModel):
    tool_name: str
    arguments: dict[str, Any]


class SkillMCPBridger(BaseSkill):
    """
    Skill that bridges Swarm Workers to external MCP servers.
    Useful for executing tools like 'post_content' or 'search_trends' via MCP.
    """

    def __init__(self, mcp_client):
        self._mcp_client = mcp_client

    @property
    def name(self) -> str:
        return "skill_mcp_bridger"

    async def execute(self, task_input: WorkerTaskInput) -> WorkerTaskOutput:
        if not self._mcp_client:
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=self.name,
                result=None,
                confidence_score=0.0,
                reasoning="MCP client not initialized on this brider.",
            )

        try:
            params = MCPToolInput(**task_input.params)
            mcp_result = await self._mcp_client.call_tool(params.tool_name, params.arguments)

            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=self.name,
                result={"mcp_output": mcp_result},
                confidence_score=1.0,
                reasoning=f"Successfully executed MCP tool: {params.tool_name}",
            )
        except Exception as e:
            return WorkerTaskOutput(
                task_id=task_input.task_id,
                skill_name=self.name,
                result=None,
                confidence_score=0.0,
                reasoning=f"MCP bridge execution failed: {str(e)}",
            )

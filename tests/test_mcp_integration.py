import asyncio
import os
import subprocess
import time
from uuid import uuid4

import pytest

from skills.skill_mcp_bridger import SkillMCPBridger
from src.mcp.client import ChimeraMCPClient
from src.models.schemas import WorkerTaskInput


@pytest.mark.asyncio
async def test_mcp_client_connectivity():
    # We will run the mock server using 'python mcp-server-mock/server.py'
    # For a stdio client, we pass the command directly
    server_script = os.path.abspath("mcp-server-mock/server.py")
    client = ChimeraMCPClient(command="python", args=[server_script])

    await client.connect()

    # Test tool calling directly
    result = await client.call_tool("search_trends", {"topic": "AI Agents"})
    assert "TRENDS" in result[0].text
    assert "agents" in result[0].text

    await client.disconnect()


@pytest.mark.asyncio
async def test_worker_mcp_bridger_skill():
    server_script = os.path.abspath("mcp-server-mock/server.py")
    client = ChimeraMCPClient(command="python", args=[server_script])
    await client.connect()

    bridger = SkillMCPBridger(mcp_client=client)

    task_input = WorkerTaskInput(
        task_id=uuid4(),
        skill_name="skill_mcp_bridger",
        params={
            "tool_name": "post_content",
            "arguments": {"platform": "twitter", "content": "Testing MCP Swarm Integration!"},
        },
        persona_id="p1",
    )

    output = await bridger.execute(task_input)

    assert output.confidence_score == 1.0
    assert "SUCCESS" in output.result["mcp_output"][0].text

    await client.disconnect()

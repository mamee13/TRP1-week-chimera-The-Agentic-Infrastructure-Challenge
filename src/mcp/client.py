import logging
from contextlib import AsyncExitStack
from typing import Any

from mcp.client.stdio import stdio_client

from mcp import ClientSession, StdioServerParameters


class ChimeraMCPClient:
    """Wrapper for MCP sessions to facilitate tool calling by swarm agents."""

    def __init__(self, command: str, args: list | None = None):
        self.server_params = StdioServerParameters(command=command, args=args or [])
        self.session: ClientSession | None = None
        self._exit_stack: AsyncExitStack | None = None

    async def connect(self):
        """Establish connection with the MCP server."""
        try:
            self._exit_stack = AsyncExitStack()
            _, write = await self._exit_stack.enter_async_context(stdio_client(self.server_params))
            self.session = await self._exit_stack.enter_async_context(ClientSession(_, write))
            if self.session:
                await self.session.initialize()
            logging.info("MCP Client connected and initialized.")
        except Exception as e:
            logging.error(f"Failed to connect to MCP server: {str(e)}")
            raise

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call a specific tool on the connected MCP server."""
        if not self.session:
            raise RuntimeError("MCP Client is not connected.")

        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result.content
        except Exception as e:
            logging.error(f"Error calling tool {tool_name}: {str(e)}")
            raise

    async def disconnect(self):
        """Cleanly disconnect from the MCP server."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            logging.info("MCP Client disconnected.")

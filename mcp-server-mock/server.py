from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Chimera Mock Social Server")

@mcp.tool()
def post_content(platform: str, content: str) -> str:
    """Post content to a social media platform (Mock)."""
    return f"SUCCESS: Posted to {platform}: {content[:50]}..."

@mcp.tool()
def search_trends(topic: str) -> str:
    """Search for trends related to a topic (Mock)."""
    return f"TRENDS for {topic}: agents, tech, automation, ethiopia"

if __name__ == "__main__":
    mcp.run()

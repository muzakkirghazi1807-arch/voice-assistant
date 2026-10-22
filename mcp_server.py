"""Small, safe MCP tools for the JARVIS project."""
from datetime import datetime

from mcp.server import MCPServer

server = MCPServer("JARVIS")


@server.tool()
def get_current_datetime() -> str:
    """Get the computer's current local date, time, and time zone."""
    return datetime.now().astimezone().strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")


@server.tool()
def jarvis_greeting() -> str:
    """Check that the JARVIS MCP server is running and get a greeting."""
    return "JARVIS MCP is online and ready. Your Flask and Gemini app runs separately."


if __name__ == "__main__":
    # MCP stdio uses stdout for protocol messages; keep this entry point quiet.
    server.run(transport="stdio")

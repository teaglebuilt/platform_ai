import sys
import logging
import traceback

from mcp.server.fastmcp import FastMCP
from interfaces.mcp_definitions import CommandHelpResult

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

mcp_server = FastMCP("MCP Server")


@mcp_server.tool()
async def research_codebase(args: dict) -> CommandHelpResult:
    try:
        sys.stderr.write(f"Tool called with args: {args}\n")
        return CommandHelpResult(help_text="Tool ran successfully", status="success")
    except Exception as e:
        sys.stderr.write("Exception in tool:\n")
        traceback.print_exc(file=sys.stderr)
        return CommandHelpResult(help_text=str(e), status="error")


if __name__ == "__main__":
    mcp_server.run(transport='stdio')

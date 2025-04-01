from mcp.server.fastmcp import FastMCP
import httpx

mcp_server = FastMCP("MCP Server")
agent_server = "http://localhost:5000/api"
headers = {
    "Content-Type": "application/json"
}


@mcp_server.tool()
async def research_codebase(args: dict) -> str:
    print("args", args)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{agent_server}/research", headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


if __name__ == "__main__":
    mcp_server.run(transport='stdio')

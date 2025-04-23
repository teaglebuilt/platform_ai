import asyncio

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from fastapi import FastAPI
from starlette.routing import Mount

mcp_server = FastMCP("MCP Server")


def mount_sse_service(app: FastAPI) -> FastAPI:
    sse = SseServerTransport("/mcp/messages/")

    app.mount("/mcp", mcp_server.sse_app())
    app.router.routes.append(Mount("/mcp/messages", app=sse.handle_post_message))
    return app


@mcp_server.tool()
def research_repository():
    return {"message": "works"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metadata import VERSION, TAGS
from lifespan import service_lifespan
from mcp.server.fastmcp import FastMCP

def create_service() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    service = FastAPI(
        title="AI Platform Service",
        description="",
        version=VERSION,
        # lifespan=service_lifespan,
        openapi_tags=TAGS,
    )
    # mcp_server = FastMCP("MCP Server")
    # service.mount("/mcp", mcp_server.sse_app())
    return service


api = create_service()


api.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


api.post("/webhook")
def webhook_event():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=3000)

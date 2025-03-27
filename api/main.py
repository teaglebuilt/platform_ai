from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.metadata import VERSION, TAGS
from api.lifespan import service_lifespan

def create_service() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    service = FastAPI(
        title="MCP Bridge",
        description="A middleware application to add MCP support to OpenAI-compatible APIs",
        version=VERSION,
        lifespan=service_lifespan,
        openapi_tags=TAGS,
    )
    return service

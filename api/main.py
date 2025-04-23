from fastapi import FastAPI
from metadata import VERSION, TAGS
from lifespan import service_lifespan
from services.mcp_service import mount_sse_service
from services.cost_metrics import metrics_app

def create_service() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    service = FastAPI(
        title="AI Platform Service",
        description="",
        version=VERSION,
        lifespan=service_lifespan,
        openapi_tags=TAGS,
    )
    # service_with_mcp_routes = mount_sse_service(service)
    return service


platform_api = create_service()


platform_api.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


platform_api.post("/webhook")
def webhook_event():
    pass



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(platform_api, host="0.0.0.0", port=8000)

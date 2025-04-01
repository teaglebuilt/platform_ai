from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.metadata import VERSION, TAGS
from api.lifespan import service_lifespan

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
    return service

api = create_service()


api.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


api.post("/webhook")
def webhook_event():
    pass

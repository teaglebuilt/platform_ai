from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from api.services.research import ResearchService

research_router = APIRouter()


class ResearchTaskRequest(BaseModel):
    pass


class ResearchTaskResponse(BaseModel):
    pass


research_router.post("/research", response_model=ResearchTaskResponse)
def run_research_task(request: ResearchTaskRequest, background_tasks: BackgroundTasks):
    task_id = uuid4()
    background_tasks.add_task(ResearchService.process_task, task_id, request.topic)
    return ResearchService.get_task_status(task_id)

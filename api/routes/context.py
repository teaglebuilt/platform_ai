from fastapi import APIRouter
from pydantic import BaseModel

context_router = APIRouter()


class ContextProviderInput(BaseModel):
    query: str
    fullInput: str


@context_router.post("/retrieve")
async def create_item(item: ContextProviderInput):
    results = [] # TODO: Query your vector database here.
    print(item)
    # Construct the "context item" format expected by Continue
    context_items = []
    for result in results:
        context_items.append({
            "name": result.filename,
            "description": result.filename,
            "content": result.text,
        })

    return context_items
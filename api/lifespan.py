import asyncio
from typing import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from services.cost_metrics import metric_scheduler


@asynccontextmanager
async def service_lifespan(server: FastAPI) -> AsyncIterator[None]:
    task = asyncio.create_task(metric_scheduler())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

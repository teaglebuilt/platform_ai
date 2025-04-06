from typing import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from interfaces.service_context import ServiceContext

@asynccontextmanager
async def service_lifespan(server: FastAPI) -> AsyncIterator[ServiceContext]:
    pass

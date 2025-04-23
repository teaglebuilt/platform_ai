from typing import TypeVar

from fastapi import FastAPI

AppType = TypeVar("AppType", bound=FastAPI)
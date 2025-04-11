from typing import Literal

from langsmith import Client as LangSmithClient


def get_langsmith_tracer() -> LangSmithClient:
    return LangSmithClient()


def get_tracer(tracer: Literal["langsmith", "openlit"]):
    tracers = {
        "langsmith": get_langsmith_tracer
    }
    return tracers[tracer]()

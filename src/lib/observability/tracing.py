from typing import Literal

from langsmith import Client as LangSmithClient


def get_langsmith_tracer() -> LangSmithClient:
    return LangSmithClient()


def get_openlit_tracer():
    import openlit
    openlit.init(otlp_endpoint="http://127.0.0.1:4318")
    return openlit.trace


def get_tracer(tracer: Literal["langsmith", "openlit"]):
    tracers = {
        "langsmith": get_langsmith_tracer,
        "openlit": get_openlit_tracer
    }
    return tracers[tracer]()

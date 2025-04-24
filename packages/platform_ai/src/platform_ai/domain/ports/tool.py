from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class Tool(Protocol):
    name: str
    description: str

    def execute(self, **kwargs: Any) -> Any:
        ...



@runtime_checkable
class ToolProvider(Protocol):
    def get_tools(self, type: str, feature_path: str) -> list[Tool]:
        ...

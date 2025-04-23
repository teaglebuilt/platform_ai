from typing import Protocol, TypedDict, runtime_checkable


class GatewayResponse(TypedDict):
    status_code: int
    content: str
    error: str


@runtime_checkable
class AIGateway(Protocol):

    def chat(self, agent_name: str, message: str) -> str:
        ...

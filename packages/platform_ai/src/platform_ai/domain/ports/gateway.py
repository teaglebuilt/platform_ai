from typing import Protocol, TypedDict, runtime_checkable, TypeVar, Iterator

ModelT = TypeVar("ModelT", bound=str, contravariant=True)


class GatewayResponse(TypedDict):
    status_code: int
    content: str
    error: str


@runtime_checkable
class AIGateway(Protocol[ModelT]):

    def chat(self, model: ModelT, message: str) -> str:
        ...

    def stream_chat(self, model: ModelT, message: str) -> Iterator[str]:
        ...

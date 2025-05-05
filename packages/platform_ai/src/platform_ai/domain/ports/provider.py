from typing import Protocol, runtime_checkable, Iterator, TypeVar


ModelT = TypeVar("ModelT", bound=str, contravariant=True)


@runtime_checkable
class LLMProvider(Protocol[ModelT]):

    def __init__(self, llm: ModelT) -> None:
        ...

    @property
    def model_name(self) -> str:
        ...

    @property
    def host_url(self) -> str:
        ...

    def chat(self, model: ModelT, message: str) -> str:
        ...

    def stream_chat(self, model: ModelT, message: str) -> Iterator[str]:
        ...

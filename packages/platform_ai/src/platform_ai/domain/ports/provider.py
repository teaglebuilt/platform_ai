from typing import Protocol, runtime_checkable, Iterator, TypeVar


ModelT = TypeVar("ModelT", bound=str, contravariant=True)


@runtime_checkable
class LLMProvider(Protocol[ModelT]):

    def chat(self, model: ModelT, message: str) -> str:
        ...

    def stream_chat(self, model: ModelT, message: str) -> Iterator[str]:
        ...

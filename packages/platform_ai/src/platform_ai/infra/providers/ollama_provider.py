from typing import Iterator, Literal

from langchain_ollama import ChatOllama
from platform_ai.domain.ports.provider import LLMProvider

OllamaModels = Literal["llama3:latest"]

class OllamaProvider(LLMProvider[OllamaModels]):

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def chat(self, model: OllamaModels, message: str) -> str:
        llm = ChatOllama(model=model, base_url=self.base_url)
        response = llm.invoke(message)
        return response.model_dump_json()

    def stream_chat(self, model: OllamaModels, message: str) -> Iterator[str]:
        llm = ChatOllama(model=model, base_url=self.base_url)
        for chunk in llm.stream(message):
            yield chunk.model_dump_json()

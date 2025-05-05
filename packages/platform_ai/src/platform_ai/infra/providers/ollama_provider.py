import os
from typing import Iterator, Literal, Optional

from langchain_ollama import ChatOllama
from platform_ai.domain.ports.provider import LLMProvider

OllamaModels = Literal["llama3:latest"]

class OllamaProvider(LLMProvider[OllamaModels]):

    def __init__(
        self,
        llm: str,
        base_url: str = os.environ['OLLAMA_HOST'],
        api_key: Optional[str] = None
    ) -> None:
        self.llm = llm
        self.base_url = base_url
        self.api_key = api_key

    @property
    def model_name(self):
        return self.llm

    @property
    def host_url(self):
        return self.base_url

    def chat(self, model: OllamaModels, message: str) -> str:
        llm = ChatOllama(model=model, base_url=self.base_url)
        response = llm.invoke(message)
        return response.model_dump_json()

    def stream_chat(self, model: OllamaModels, message: str) -> Iterator[str]:
        llm = ChatOllama(model=model, base_url=self.base_url)
        for chunk in llm.stream(message):
            yield chunk.model_dump_json()

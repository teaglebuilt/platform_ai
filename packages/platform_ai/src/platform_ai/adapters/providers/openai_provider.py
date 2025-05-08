import os
from typing import Iterator, Literal, Optional

from openai import OpenAI

from platform_ai.domain.ports.provider import LLMProvider

OpenAIModels = Literal["gpt-3.5-turbo", "gpt-4o"]


class OpenAIProvider(LLMProvider[OpenAIModels]):
    def __init__(
        self,
        llm: OpenAIModels,
        api_key: Optional[str] = None
    ) -> None:
        self.llm = llm
        self.base_url = os.environ["AI_GATEWAY_HOST"]
        self.client = OpenAI(base_url=self.base_url, api_key=api_key)

    @property
    def model_name(self):
        return self.llm

    @property
    def host_url(self):
        return self.base_url

    def chat(self, model: OpenAIModels, message: str) -> str:
        response = self.client.chat.completions.with_raw_response.create(
            messages=[{"role": "user", "content": message}],
            model=model
        )
        return str(response.content)

    def stream_chat(self, model: OpenAIModels, message: str) -> Iterator[str]:
        with self.client.chat.completions.with_streaming_response.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        ) as response:
            for line in response.iter_lines():
                yield line

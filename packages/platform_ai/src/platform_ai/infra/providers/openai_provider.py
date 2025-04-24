from typing import Iterator, Literal

from openai import OpenAI

from platform_ai.domain.ports.provider import LLMProvider

OpenAIModels = Literal["gpt-3.5-turbo", "gpt-4o"]


class OpenAIProvider(LLMProvider[OpenAIModels]):
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

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

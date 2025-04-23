from typing import Iterator

from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types import ChatModel


class OpenAIProviderGateway:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

    def chat(self, model: ChatModel, message: str) -> str:
        response = self.client.chat.completions.with_raw_response.create(
            messages=[{"role": "user", "content": message}],
            model=model
        )
        return str(response.content)

    def stream_chat(self, model: ChatModel, message: str) -> Iterator[str]:
        with self.client.chat.completions.with_streaming_response.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        ) as response:
            for line in response.iter_lines():
                yield line

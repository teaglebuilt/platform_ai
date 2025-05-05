from typing import Iterator, AsyncIterator, Union

import httpx

from platform_ai.domain.ports.gateway import AIGateway
from platform_ai.infra.providers.openai_provider import OpenAIModels
from platform_ai.infra.providers.ollama_provider import OllamaModels

LLModel = Union[OpenAIModels, OllamaModels]


class EnvoyAIGateway(AIGateway[LLModel]):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {
            # "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, model: LLModel, message: str) -> str:
        self.headers["x-ai-eg-model"] = model

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        with httpx.Client() as client:
            response = client.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    def stream_chat(self, model: LLModel, message: str) -> Iterator[str]:
        self.headers["x-ai-eg-model"] = model

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        with httpx.Client() as client:
            with client.stream("POST", self.base_url, headers=self.headers, json=payload) as response:
                response.raise_for_status()
                for line in response.iter_text():
                    if line.startswith("data: "):
                        yield line.removeprefix("data: ").strip()

    async def stream_chat_async(self, model: LLModel, message: str) -> AsyncIterator[str]:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.base_url, headers=self.headers, json=payload) as response:
                async for line in response.aiter_lines():
                    yield line

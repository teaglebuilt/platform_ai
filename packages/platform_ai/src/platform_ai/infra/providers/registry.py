from typing import Union, Type, Literal
from platform_ai.domain.ports.provider import LLMProvider
from platform_ai.infra.providers.ollama_provider import OllamaProvider
from platform_ai.infra.providers.openai_provider import OpenAIProvider

ChatModelType = Union[OllamaProvider, OpenAIProvider]

MODEL_PROVIDER_MAP: dict[str, Type[LLMProvider]] = {
    "gpt-4": OpenAIProvider,
    "gpt-4o": OpenAIProvider,
    "gpt-4.1-mini": OpenAIProvider,
    "llama-3": OllamaProvider,
    "llama-3.3-70b": OllamaProvider,
    "deepseek-coder-v2:latest": OllamaProvider,
    "qwen2.5-coder:latest": OllamaProvider,
    "llama-3.3-70b-instruct": OllamaProvider
}


def resolve_llm_provider(llm_name: str) -> Type[LLMProvider] | None:
    for key, cls in MODEL_PROVIDER_MAP.items():
        if llm_name == key:
            return cls
    raise ValueError(f"No matching provider found for LLM: {llm_name}")


def get_llm_provider(llm_name: str) -> LLMProvider:
    provider = resolve_llm_provider(llm_name)
    if not provider:
        raise ValueError("No provider was found")
    return provider(llm=llm_name)

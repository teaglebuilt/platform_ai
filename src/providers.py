from langchain_community import chat_models
from enum import Enum
from typing import Any


class LLMProvider(Enum):
    OPENAI = "ChatOpenAI"
    ANTHROPIC = "ChatAnthropic"
    GOOGLE = "ChatGoogle"


def get_llm_provider(provider: LLMProvider) -> Any:
    try:
        provider_class = getattr(chat_models, provider.value)
        return provider_class()
    except AttributeError as e:
        raise ValueError(f"Provider '{provider.value}' not found in chat_models module.") from e

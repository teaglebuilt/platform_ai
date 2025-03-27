from typing import Union
from langchain_community import chat_models
from langchain_community.chat_models import ChatOllama, ChatOpenAI, ChatAnthropic
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "ChatOpenAI"
    ANTHROPIC = "ChatAnthropic"
    OLLAMA = "ChatOllama"

ChatModelType = Union[ChatOllama, ChatOpenAI, ChatAnthropic]

def get_llm_provider(provider: LLMProvider) -> ChatModelType:
    try:
        provider_class = getattr(chat_models, provider.value)
        return provider_class()
    except AttributeError as e:
        raise ValueError(f"Provider '{provider.value}' not found in chat_models module.") from e

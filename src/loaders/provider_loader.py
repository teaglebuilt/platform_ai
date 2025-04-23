import os
from enum import Enum
from typing import Union, Type, Literal

from langchain_core.callbacks import CallbackManager, BaseCallbackHandler
from langchain_community.chat_models import ChatOllama, ChatOpenAI, ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from crewai.llm import LLM

ChatModelType = Union[ChatOllama, ChatOpenAI, ChatAnthropic]


class LLMProvider(Enum):
    OPENAI = ChatOpenAI
    ANTHROPIC = ChatAnthropic
    OLLAMA = ChatOllama


MODEL_PROVIDER_MAP: dict[str, Type[BaseChatModel]] = {
    "gpt-4": ChatOpenAI,
    "gpt-4o": ChatOpenAI,
    "gpt-4.1-mini": ChatOpenAI,
    "llama-3": ChatOllama,
    "llama-3.3-70b": ChatOllama,
    "claude-3": ChatAnthropic,
    "claude-3-opus": ChatAnthropic,
    "deepseek-coder-v2:latest": ChatOllama,
    "qwen2.5-coder:latest": ChatOllama,
    "llama-3.3-70b-instruct": ChatOllama
}


def resolve_llm_provider(llm_name: Literal["gpt-4o"]) -> Type[BaseChatModel] | None:
    for key, cls in MODEL_PROVIDER_MAP.items():
        if llm_name == key:
            return cls
    raise ValueError(f"No matching provider found for LLM: {llm_name}")


def get_llm_provider(
    llm: Literal["gpt-4o"],
    trace_with: Literal["langsmith", "openlit", "none"] = "none",
    **kwargs
) -> LLM | None:
    provider = resolve_llm_provider(llm)
    if not provider:
        raise ValueError("No provider was found")
    # callbacks = [ProviderCostTrackingCallbackHandler()]
    # if trace_with != "none":
    #     tracer = get_tracer(trace_with)
    #     callbacks.append(tracer)
    if isinstance(provider, ChatOllama):
        return LLM(
            model=llm,
            base_url="https://ollama.homelab.internal",
            **kwargs
        )
    if isinstance(provider, ChatOpenAI):
        cost_tracker = ProviderCostTrackingCallbackHandler()
        return LLM(
            model=llm,
            temperature=0,
            messages=[],
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=f"http://{os.environ["AI_GATEWAY_IP"]}",
            callback_manager=CallbackManager([cost_tracker]),
            **kwargs
        )


class ProviderCostTrackingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        # self.project_budget = get_project_budget()

    def on_llm_end(self, response, **kwargs):
        usage = response.llm_output.get("token_usage", {})
        prompt = usage.get("prompt_tokens", 0)
        completion = usage.get("completion_tokens", 0)
        total = usage.get("total_tokens", 0)
        self.total_tokens += total

        # OpenAI GPT-4 Turbo cost example
        cost = (prompt / 1000 * 0.01) + (completion / 1000 * 0.03)
        self.total_cost += cost

        print(f"[Cost] Prompt: {prompt}, Completion: {completion}, Cost: ${cost:.4f}, Total: ${self.total_cost:.4f}")
        # if self.total_cost >= self.project_budget:
        #     print(f"⚠️ Budget Alert: Total cost ${self.total_cost:.2f} has reached or exceeded the project budget of ${self.project_budget:.2f}!")

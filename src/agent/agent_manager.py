from typing import TypedDict, Union, Literal, Callable
from crewai import Agent as CrewAIAgent
from agents import Agent as OpenAIAgent
from agents.mcp import MCPServer

AgentType = Union[CrewAIAgent, OpenAIAgent]

class AgentConfig(TypedDict):
    name: str
    provider: Literal["crewai", "openagent"]
    instructions: str
    mcp_servers: list[MCPServer] = list


AgentFactory = Callable[[AgentConfig], AgentType]
agent_registry: dict[str, AgentFactory] = {}


def register_agent_type(name: str):
    def wrapper(fn: AgentFactory):
        agent_registry[name] = fn
        return fn
    return wrapper


@register_agent_type("crewai")
def create_crewai_agent(config: AgentConfig) -> CrewAIAgent:
    return CrewAIAgent(name=config.name, instructions=config.instructions)


@register_agent_type("openagents")
def create_openagents_agent(config: AgentConfig) -> OpenAIAgent:
    return OpenAIAgent(name=config.name, instructions=config.instructions, mcp_servers=config.mcp_servers)


def get_agent(config: AgentConfig) -> AgentType:
    creator = agent_registry.get(config.provider)
    if not creator:
        raise ValueError(f"No agent factory for provider '{config.provider}'")
    return creator(config)

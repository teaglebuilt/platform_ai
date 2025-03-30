from typing import TypedDict
from agents import Agent
from agents.mcp import MCPServer


class AgentConfig(TypedDict):
    name: str
    instructions: str
    mcp_servers: list[MCPServer] = list


def get_agent(config: AgentConfig) -> Agent:
    return Agent(**config)


class AgentManager:
    pass

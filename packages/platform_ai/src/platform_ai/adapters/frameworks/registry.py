from enum import Enum

from platform_ai.adapters.frameworks.crewai.crewai_adapter import CrewAdapter
from platform_ai.domain.ports.framework import AgentFramework


class FrameworkRegistry(Enum):
    CREWAI = "crewai"


def select_framework(framework: str) -> AgentFramework:
    match framework:
        case FrameworkRegistry.CREWAI.value:
            return CrewAdapter()
        case _:
            raise ValueError(f"Unsupported framework: {framework}")

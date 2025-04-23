from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.agent import Agent


class AgentRepository(ABC):

    @abstractmethod
    def save(self, agent: Agent) -> None:
        pass

    @abstractmethod
    def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        pass

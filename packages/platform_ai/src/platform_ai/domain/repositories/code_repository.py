from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from platform_ai.domain.models.code import CodeChunk


class CodeRepository(ABC):

    @abstractmethod
    def save(self, code: CodeChunk) -> None:
        pass

    @abstractmethod
    def index(self, file: str) -> None:
        pass

from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class Agent:
    id: UUID
    name: str
    description: Optional[str] = None
    metadata: dict | None = None

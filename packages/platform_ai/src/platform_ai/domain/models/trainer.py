from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class TrainerConfig:
    type: Literal["agent", "model"]
    framework: Literal["crewai", "langchain", "huggingface"]
    config_path: Optional[str] = None
    verbose: bool = False

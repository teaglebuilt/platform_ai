from typing import Protocol, runtime_checkable


@runtime_checkable
class Sandbox(Protocol):
    def run_code(self, code: str, language: str = "python") -> None:
from typing import Protocol


class EventHandler(Protocol):
    def handle_event(self, event_type: str, payload: dict):
        ...


class CommandHandler(Protocol):
    def handle_command(self, command_type: str, payload: dict):
        ...

from typing import Protocol
from abc import abstractmethod


class RoutingStrategy(Protocol):

    @abstractmethod
    def route(self):
        pass

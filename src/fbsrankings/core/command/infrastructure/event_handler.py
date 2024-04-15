from abc import ABCMeta
from abc import abstractmethod
from typing import ContextManager

from typing_extensions import Protocol

from fbsrankings.common import EventBus


class EventHandler(ContextManager["EventHandler"], metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class EventHandlerFactory(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def event_handler(self, event_bus: EventBus) -> EventHandler:
        raise NotImplementedError

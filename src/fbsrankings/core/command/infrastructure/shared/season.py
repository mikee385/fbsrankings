from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from fbsrankings.messages.event import SeasonCreatedEvent


class SeasonEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_created(self, event: SeasonCreatedEvent) -> None:
        raise NotImplementedError


class SeasonEventManager(ContextManager["SeasonEventManager"]):
    def __init__(self, handler: SeasonEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(SeasonCreatedEvent, self._handler.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(SeasonCreatedEvent, self._handler.handle_created)

    def __enter__(self) -> "SeasonEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

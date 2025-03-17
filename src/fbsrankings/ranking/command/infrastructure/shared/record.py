from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRecordCalculatedEvent


class TeamRecordEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        raise NotImplementedError


class TeamRecordEventManager(ContextManager["TeamRecordEventManager"]):
    def __init__(self, handler: TeamRecordEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(
            TeamRecordCalculatedEvent,
            self._handler.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRecordCalculatedEvent,
            self._handler.handle_calculated,
        )

    def __enter__(self) -> "TeamRecordEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

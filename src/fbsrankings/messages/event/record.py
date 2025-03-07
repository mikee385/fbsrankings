from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type

from dataclasses import dataclass
from typing_extensions import Literal

from communication.bus import EventBus
from communication.messages import Event


@dataclass(frozen=True)
class TeamRecordValue:
    team_id: str
    wins: int
    losses: int
    games: int
    win_percentage: float


@dataclass(frozen=True)
class TeamRecordCalculatedEvent(Event):
    event_id: str
    record_id: str
    season_id: str
    week: Optional[int]
    values: List[TeamRecordValue]


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
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type
from uuid import UUID

from dataclasses import dataclass
from typing_extensions import Literal

from communication.bus import Event
from communication.bus import EventBus


@dataclass(frozen=True)
class RankingValue:
    id_: UUID
    order: int
    rank: int
    value: float


@dataclass(frozen=True)  # noqa: B024
class RankingCalculatedEvent(Event, metaclass=ABCMeta):
    id_: UUID
    name: str
    season_id: UUID
    week: Optional[int]
    values: List[RankingValue]


@dataclass(frozen=True)
class TeamRankingCalculatedEvent(RankingCalculatedEvent):
    pass


class TeamRankingEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_calculated(self, event: TeamRankingCalculatedEvent) -> None:
        raise NotImplementedError


class TeamRankingEventManager(ContextManager["TeamRankingEventManager"]):
    def __init__(self, handler: TeamRankingEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(
            TeamRankingCalculatedEvent,
            self._handler.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRankingCalculatedEvent,
            self._handler.handle_calculated,
        )

    def __enter__(self) -> "TeamRankingEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


@dataclass(frozen=True)
class GameRankingCalculatedEvent(RankingCalculatedEvent):
    pass


class GameRankingEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        raise NotImplementedError


class GameRankingEventManager(ContextManager["GameRankingEventManager"]):
    def __init__(self, handler: GameRankingEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(
            GameRankingCalculatedEvent,
            self._handler.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            GameRankingCalculatedEvent,
            self._handler.handle_calculated,
        )

    def __enter__(self) -> "GameRankingEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.event import TeamRankingCalculatedEvent


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
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


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
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

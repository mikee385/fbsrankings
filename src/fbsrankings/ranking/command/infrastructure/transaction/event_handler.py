from types import TracebackType
from typing import List
from typing import Optional
from typing import Type

from typing_extensions import Literal

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.messages.event import GameRankingEventManager
from fbsrankings.messages.event import TeamRankingEventManager
from fbsrankings.messages.event import TeamRecordEventManager
from fbsrankings.ranking.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.ranking.command.infrastructure.transaction.ranking import (
    GameRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.transaction.ranking import (
    TeamRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.transaction.record import (
    TeamRecordEventHandler,
)


class EventHandler(BaseEventHandler):
    def __init__(self, event_bus: EventBus, cache_bus: EventBus) -> None:
        self.events: List[Event] = []

        self._team_record = TeamRecordEventManager(
            TeamRecordEventHandler(self.events, cache_bus),
            event_bus,
        )
        self._team_ranking = TeamRankingEventManager(
            TeamRankingEventHandler(self.events, cache_bus),
            event_bus,
        )
        self._game_ranking = GameRankingEventManager(
            GameRankingEventHandler(self.events, cache_bus),
            event_bus,
        )

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        self.clear()

    def clear(self) -> None:
        self.events.clear()

    def __enter__(self) -> "EventHandler":
        self._team_record.__enter__()
        self._team_ranking.__enter__()
        self._game_ranking.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        self._game_ranking.__exit__(type_, value, traceback)
        self._team_ranking.__exit__(type_, value, traceback)
        self._team_record.__exit__(type_, value, traceback)
        return False

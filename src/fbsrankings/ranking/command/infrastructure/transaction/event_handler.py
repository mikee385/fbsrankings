from typing import List

from fbsrankings.common import Event
from fbsrankings.common import EventBus
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

        self._team_record = TeamRecordEventHandler(self.events, event_bus, cache_bus)
        self._team_ranking = TeamRankingEventHandler(self.events, event_bus, cache_bus)
        self._game_ranking = GameRankingEventHandler(self.events, event_bus, cache_bus)

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        self.clear()

    def clear(self) -> None:
        self.events.clear()

from typing import List

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.core.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.core.command.infrastructure.transaction.affiliation import (
    AffiliationEventHandler,
)
from fbsrankings.core.command.infrastructure.transaction.game import GameEventHandler
from fbsrankings.core.command.infrastructure.transaction.season import (
    SeasonEventHandler,
)
from fbsrankings.core.command.infrastructure.transaction.team import TeamEventHandler


class EventHandler(BaseEventHandler):
    def __init__(self, event_bus: EventBus, cache_bus: EventBus) -> None:
        self.events: List[Event] = []

        self._season = SeasonEventHandler(self.events, event_bus, cache_bus)
        self._team = TeamEventHandler(self.events, event_bus, cache_bus)
        self._affiliation = AffiliationEventHandler(self.events, event_bus, cache_bus)
        self._game = GameEventHandler(self.events, event_bus, cache_bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self.clear()

    def clear(self) -> None:
        self.events.clear()

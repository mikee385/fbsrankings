from types import TracebackType
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.core.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.core.command.infrastructure.shared.affiliation import (
    AffiliationEventManager,
)
from fbsrankings.core.command.infrastructure.shared.game import GameEventManager
from fbsrankings.core.command.infrastructure.shared.season import SeasonEventManager
from fbsrankings.core.command.infrastructure.shared.team import TeamEventManager
from fbsrankings.core.command.infrastructure.transaction.affiliation import (
    AffiliationEventHandler,
)
from fbsrankings.core.command.infrastructure.transaction.game import GameEventHandler
from fbsrankings.core.command.infrastructure.transaction.season import (
    SeasonEventHandler,
)
from fbsrankings.core.command.infrastructure.transaction.team import TeamEventHandler


class EventHandler(BaseEventHandler):
    def __init__(
        self,
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        self.events: list[Event] = []

        self._season = SeasonEventManager(
            SeasonEventHandler(self.events, cache_bus),
            event_bus,
        )
        self._team = TeamEventManager(
            TeamEventHandler(self.events, cache_bus),
            event_bus,
        )
        self._affiliation = AffiliationEventManager(
            AffiliationEventHandler(self.events, cache_bus),
            event_bus,
        )
        self._game = GameEventManager(
            GameEventHandler(self.events, cache_bus),
            event_bus,
        )

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self.clear()

    def clear(self) -> None:
        self.events.clear()

    def __enter__(self) -> "EventHandler":
        self._season.__enter__()
        self._team.__enter__()
        self._affiliation.__enter__()
        self._game.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        self._game.__exit__(type_, value, traceback)
        self._affiliation.__exit__(type_, value, traceback)
        self._team.__exit__(type_, value, traceback)
        self._season.__exit__(type_, value, traceback)
        return False

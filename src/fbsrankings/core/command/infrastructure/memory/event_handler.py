from types import TracebackType
from typing import Optional
from typing import Type

from typing_extensions import Literal

from communication.bus import EventBus
from fbsrankings.core.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.core.command.infrastructure.memory.affiliation import (
    AffiliationEventHandler,
)
from fbsrankings.core.command.infrastructure.memory.game import GameEventHandler
from fbsrankings.core.command.infrastructure.memory.season import SeasonEventHandler
from fbsrankings.core.command.infrastructure.memory.team import TeamEventHandler
from fbsrankings.messages.event import AffiliationEventManager
from fbsrankings.messages.event import GameEventManager
from fbsrankings.messages.event import SeasonEventManager
from fbsrankings.messages.event import TeamEventManager
from fbsrankings.storage.memory import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._season = SeasonEventManager(SeasonEventHandler(storage.season), bus)
        self._team = TeamEventManager(TeamEventHandler(storage.team), bus)
        self._affiliation = AffiliationEventManager(
            AffiliationEventHandler(storage.affiliation),
            bus,
        )
        self._game = GameEventManager(GameEventHandler(storage.game), bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

    def __enter__(self) -> "EventHandler":
        self._season.__enter__()
        self._team.__enter__()
        self._affiliation.__enter__()
        self._game.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        self._game.__exit__(type_, value, traceback)
        self._affiliation.__exit__(type_, value, traceback)
        self._team.__exit__(type_, value, traceback)
        self._season.__exit__(type_, value, traceback)
        return False

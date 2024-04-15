import sqlite3
from types import TracebackType
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.core.command.event.affiliation import (
    AffiliationEventManager,
)
from fbsrankings.core.command.event.game import GameEventManager
from fbsrankings.core.command.event.season import SeasonEventManager
from fbsrankings.core.command.event.team import TeamEventManager
from fbsrankings.core.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.core.command.infrastructure.sqlite.affiliation import (
    AffiliationEventHandler,
)
from fbsrankings.core.command.infrastructure.sqlite.game import GameEventHandler
from fbsrankings.core.command.infrastructure.sqlite.season import SeasonEventHandler
from fbsrankings.core.command.infrastructure.sqlite.team import TeamEventHandler
from fbsrankings.storage.sqlite import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._cursor = storage.connection.cursor()
        self._cursor.execute("begin")

        self._season = SeasonEventManager(SeasonEventHandler(self._cursor), bus)
        self._team = TeamEventManager(TeamEventHandler(self._cursor), bus)
        self._affiliation = AffiliationEventManager(
            AffiliationEventHandler(self._cursor),
            bus,
        )
        self._game = GameEventManager(GameEventHandler(self._cursor), bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        try:
            self._cursor.execute("commit")
            self._cursor.close()
        except sqlite3.ProgrammingError:
            pass

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

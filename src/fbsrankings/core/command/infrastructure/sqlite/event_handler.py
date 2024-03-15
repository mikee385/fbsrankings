import sqlite3

from fbsrankings.common import EventBus
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

        self._season = SeasonEventHandler(self._cursor, bus)
        self._team = TeamEventHandler(self._cursor, bus)
        self._affiliation = AffiliationEventHandler(self._cursor, bus)
        self._game = GameEventHandler(self._cursor, bus)

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

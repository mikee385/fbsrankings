import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.ranking.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.ranking.command.infrastructure.sqlite.ranking import (
    GameRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.sqlite.ranking import (
    TeamRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.sqlite.record import (
    TeamRecordEventHandler,
)
from fbsrankings.storage.sqlite import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._cursor = storage.connection.cursor()
        self._cursor.execute("begin")

        self._team_record = TeamRecordEventHandler(self._cursor, bus)
        self._team_ranking = TeamRankingEventHandler(self._cursor, bus)
        self._game_ranking = GameRankingEventHandler(self._cursor, bus)

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        try:
            self._cursor.execute("commit")
            self._cursor.close()
        except sqlite3.ProgrammingError:
            pass

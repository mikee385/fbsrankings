import sqlite3
from types import TracebackType
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.ranking.command.event.ranking import GameRankingEventManager
from fbsrankings.ranking.command.event.ranking import TeamRankingEventManager
from fbsrankings.ranking.command.event.record import TeamRecordEventManager
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

        self._team_record = TeamRecordEventManager(
            TeamRecordEventHandler(self._cursor),
            bus,
        )
        self._team_ranking = TeamRankingEventManager(
            TeamRankingEventHandler(self._cursor),
            bus,
        )
        self._game_ranking = GameRankingEventManager(
            GameRankingEventHandler(self._cursor),
            bus,
        )

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        try:
            self._cursor.execute("commit")
            self._cursor.close()
        except sqlite3.ProgrammingError:
            pass

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

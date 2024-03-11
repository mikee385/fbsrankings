import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.infrastructure.event_handler import EventHandler as BaseEventHandler
from fbsrankings.infrastructure.sqlite.write.affiliation import AffiliationEventHandler
from fbsrankings.infrastructure.sqlite.write.game import GameEventHandler
from fbsrankings.infrastructure.sqlite.write.ranking import GameRankingEventHandler
from fbsrankings.infrastructure.sqlite.write.ranking import TeamRankingEventHandler
from fbsrankings.infrastructure.sqlite.write.record import TeamRecordEventHandler
from fbsrankings.infrastructure.sqlite.write.season import SeasonEventHandler
from fbsrankings.infrastructure.sqlite.write.team import TeamEventHandler


class EventHandler(BaseEventHandler):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._cursor = connection.cursor()
        self._cursor.execute("begin")

        self._season = SeasonEventHandler(self._cursor, bus)
        self._team = TeamEventHandler(self._cursor, bus)
        self._affiliation = AffiliationEventHandler(self._cursor, bus)
        self._game = GameEventHandler(self._cursor, bus)

        self._team_record = TeamRecordEventHandler(self._cursor, bus)
        self._team_ranking = TeamRankingEventHandler(self._cursor, bus)
        self._game_ranking = GameRankingEventHandler(self._cursor, bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        try:
            self._cursor.execute("commit")
            self._cursor.close()
        except sqlite3.ProgrammingError:
            pass

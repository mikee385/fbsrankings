import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.infrastructure import Transaction as BaseTransaction
from fbsrankings.infrastructure.sqlite.write.affiliation import AffiliationRepository
from fbsrankings.infrastructure.sqlite.write.game import GameRepository
from fbsrankings.infrastructure.sqlite.write.ranking import GameRankingRepository
from fbsrankings.infrastructure.sqlite.write.ranking import TeamRankingRepository
from fbsrankings.infrastructure.sqlite.write.season import SeasonRepository
from fbsrankings.infrastructure.sqlite.write.team import TeamRepository


class Transaction(BaseTransaction):
    def __init__(self, database: str, bus: EventBus) -> None:
        self._bus = bus

        self._connection = sqlite3.connect(database)
        self._connection.isolation_level = None
        self._connection.execute("PRAGMA foreign_keys = ON")

        self._cursor = self._connection.cursor()
        self._cursor.execute("begin")

        self._season = SeasonRepository(self._connection, self._cursor, self._bus)
        self._team = TeamRepository(self._connection, self._cursor, self._bus)
        self._affiliation = AffiliationRepository(
            self._connection, self._cursor, self._bus
        )
        self._game = GameRepository(self._connection, self._cursor, self._bus)

        self._game_ranking = GameRankingRepository(
            self._connection, self._cursor, self._bus
        )
        self._team_ranking = TeamRankingRepository(
            self._connection, self._cursor, self._bus
        )

    @property
    def season(self) -> SeasonRepository:
        return self._season

    @property
    def team(self) -> TeamRepository:
        return self._team

    @property
    def affiliation(self) -> AffiliationRepository:
        return self._affiliation

    @property
    def game(self) -> GameRepository:
        return self._game

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

    def commit(self) -> None:
        self._cursor.execute("commit")
        self._cursor.close()
        self._connection.close()

    def rollback(self) -> None:
        self._cursor.execute("rollback")
        self._cursor.close()
        self._connection.close()

    def close(self) -> None:
        try:
            self._cursor.close()
            self._connection.close()
        except sqlite3.ProgrammingError:
            pass

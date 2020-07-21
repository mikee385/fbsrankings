import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import MostRecentCompletedWeekQuery
from fbsrankings.query import MostRecentCompletedWeekResult


class MostRecentCompletedWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.season_table = SeasonTable()
        self.game_table = GameTable()

    def __call__(
        self, query: MostRecentCompletedWeekQuery
    ) -> Optional[MostRecentCompletedWeekResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT SeasonID, Year, Week "
            + "FROM ("
            + "SELECT game.SeasonID, season.year, game.Week, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesCompleted, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesScheduled "
            + f"FROM {self.game_table.name} AS game "
            + f"INNER JOIN {self.season_table.name} AS season ON season.UUID = game.SeasonID "
            + "GROUP BY game.SeasonID, season.Year, game.Week"
            + ") AS week "
            + "WHERE GamesCompleted > 0 AND GamesScheduled == 0 "
            + "ORDER BY Year DESC, Week DESC "
            + "LIMIT 1",
            [GameStatus.COMPLETED.name, GameStatus.SCHEDULED.name],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return MostRecentCompletedWeekResult(UUID(row[0]), row[1], row[2])

        return None

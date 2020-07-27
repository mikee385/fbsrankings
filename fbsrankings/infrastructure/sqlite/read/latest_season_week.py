import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import LatestSeasonWeekQuery
from fbsrankings.query import LatestSeasonWeekResult


class LatestSeasonWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.season_table = SeasonTable()
        self.game_table = GameTable()

    def __call__(
        self, query: LatestSeasonWeekQuery
    ) -> Optional[LatestSeasonWeekResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT SeasonID, Year, GamesCompleted, GamesScheduled "
            + "FROM ("
            + "SELECT game.SeasonID, season.year, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesCompleted, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesScheduled "
            + f"FROM {self.game_table.name} AS game "
            + f"INNER JOIN {self.season_table.name} AS season ON season.UUID = game.SeasonID "
            + "GROUP BY game.SeasonID, season.Year"
            + ") AS week "
            + "WHERE GamesCompleted > 0 "
            + "ORDER BY Year DESC "
            + "LIMIT 1",
            [GameStatus.COMPLETED.name, GameStatus.SCHEDULED.name],
        )
        row = cursor.fetchone()
        cursor.close()
        
        if row is None:
            return None
            
        season_ID, year, games_completed, games_scheduled = row
            
        if games_scheduled == 0:
            return LatestSeasonWeekResult(UUID(season_ID), year, None)
        
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT Week "
            + "FROM ("
            + "SELECT game.Week, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesCompleted, "
            + "SUM(CASE WHEN game.Status == ? THEN 1 ELSE 0 END) AS GamesScheduled "
            + f"FROM {self.game_table.name} AS game "
            + "WHERE game.SeasonID = ? "
            + "GROUP BY game.Week"
            + ") AS week "
            + "WHERE GamesCompleted > 0 AND GamesScheduled == 0 "
            + "ORDER BY Week DESC "
            + "LIMIT 1",
            [GameStatus.COMPLETED.name, GameStatus.SCHEDULED.name, season_ID],
        )
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return LatestSeasonWeekResult(UUID(season_ID), year, row[0])

        return None

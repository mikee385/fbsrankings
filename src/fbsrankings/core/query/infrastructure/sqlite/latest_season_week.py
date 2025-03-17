import sqlite3
from typing import Optional

from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import LatestSeasonWeekResult
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import SeasonTable


class LatestSeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._game_table = GameTable().table

    def __call__(
        self,
        query: LatestSeasonWeekQuery,
    ) -> Optional[LatestSeasonWeekResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            "season.SeasonID, "
            "season.Year, "
            "season.GamesScheduled "
            "FROM ("
            "SELECT "
            f"{self._game_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"SUM(CASE WHEN {self._game_table}.Status = ? THEN 1 ELSE 0 END) GamesCompleted, "
            f"SUM(CASE WHEN {self._game_table}.Status = ? THEN 1 ELSE 0 END) GamesScheduled "
            f"FROM {self._game_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._game_table}.SeasonID "
            "GROUP BY "
            f"{self._game_table}.SeasonID, "
            f"{self._season_table}.Year"
            ") season "
            "WHERE season.GamesCompleted > 0 "
            "ORDER BY season.Year DESC "
            "LIMIT 1;",
            [GameStatus.GAME_STATUS_COMPLETED, GameStatus.GAME_STATUS_SCHEDULED],
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        season_id, year, games_scheduled = row

        if games_scheduled == 0:
            return LatestSeasonWeekResult(season_id=season_id, year=year, week=None)

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT week.Week "
            "FROM ("
            "SELECT Week, "
            "SUM(CASE WHEN Status = ? THEN 1 ELSE 0 END) GamesCompleted, "
            "SUM(CASE WHEN Status = ? THEN 1 ELSE 0 END) GamesScheduled "
            f"FROM {self._game_table} "
            "WHERE SeasonID = ? "
            "GROUP BY Week"
            ") week "
            "WHERE week.GamesCompleted > 0 AND week.GamesScheduled = 0 "
            "ORDER BY week.Week DESC "
            "LIMIT 1;",
            [
                GameStatus.GAME_STATUS_COMPLETED,
                GameStatus.GAME_STATUS_SCHEDULED,
                season_id,
            ],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return LatestSeasonWeekResult(season_id=season_id, year=year, week=row[0])

        return None

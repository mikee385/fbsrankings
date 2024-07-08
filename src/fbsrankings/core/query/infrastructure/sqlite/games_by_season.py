import sqlite3
from datetime import datetime
from uuid import UUID

from fbsrankings.shared.query import GameBySeasonResult
from fbsrankings.shared.query import GamesBySeasonQuery
from fbsrankings.shared.query import GamesBySeasonResult
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamTable


class GamesBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._game_table = GameTable().table

    def __call__(self, query: GamesBySeasonQuery) -> GamesBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            f"{self._game_table}.UUID, "
            f"{self._game_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"{self._game_table}.Week, "
            f"{self._game_table}.Date, "
            f"{self._game_table}.SeasonSection, "
            f"{self._game_table}.HomeTeamID, "
            "home_team.Name, "
            f"{self._game_table}.AwayTeamID, "
            "away_team.Name, "
            f"{self._game_table}.HomeTeamScore, "
            f"{self._game_table}.AwayTeamScore, "
            f"{self._game_table}.Status, "
            f"{self._game_table}.Notes "
            f"FROM {self._game_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._game_table}.SeasonID "
            f"JOIN {self._team_table} home_team "
            f"ON home_team.UUID = {self._game_table}.HomeTeamID "
            f"JOIN {self._team_table} away_team "
            f"ON away_team.UUID = {self._game_table}.AwayTeamID "
            f"WHERE {self._game_table}.SeasonID = ?;",
            [str(query.season_id)],
        )
        items = [
            GameBySeasonResult(
                UUID(row[0]),
                UUID(row[1]),
                row[2],
                row[3],
                datetime.strptime(row[4], "%Y-%m-%d").date(),
                row[5],
                UUID(row[6]),
                row[7],
                UUID(row[8]),
                row[9],
                row[10],
                row[11],
                row[12],
                row[13],
            )
            for row in cursor.fetchall()
        ]
        cursor.close()

        return GamesBySeasonResult(items)

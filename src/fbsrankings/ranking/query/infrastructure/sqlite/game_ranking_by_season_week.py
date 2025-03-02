import sqlite3
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.storage.sqlite import GameRankingValueTable
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import RankingTable
from fbsrankings.storage.sqlite import RankingType
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamTable


SqliteParam = Union[None, int, float, str, bytes]


class GameRankingBySeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._ranking_table = RankingTable().table
        self._value_table = GameRankingValueTable().table
        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._game_table = GameTable().table

    def __call__(
        self,
        query: GameRankingBySeasonWeekQuery,
    ) -> Optional[GameRankingBySeasonWeekResult]:
        sql_query = (
            "SELECT "
            f"{self._ranking_table}.UUID, "
            f"{self._ranking_table}.Name, "
            f"{self._ranking_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"{self._ranking_table}.Week "
            f"FROM {self._ranking_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._ranking_table}.SeasonID "
            f"WHERE {self._ranking_table}.Name = ? "
            f"AND {self._ranking_table}.Type = ? "
            f"AND {self._ranking_table}.SeasonID = ?"
        )

        params: List[SqliteParam] = [
            query.name,
            RankingType.GAME.name,
            str(query.season_id),
        ]

        if query.week is not None:
            sql_query += f" AND {self._ranking_table}.Week = ?;"
            params.append(query.week)
        else:
            sql_query += f" AND {self._ranking_table}.Week IS NULL;"
        cursor = self._connection.cursor()
        cursor.execute(sql_query, params)
        row = cursor.fetchone()

        values = []
        if row is not None:
            cursor.execute(
                "SELECT "
                f"{self._value_table}.GameID, "
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
                f"{self._game_table}.Notes, "
                f"{self._value_table}.Ord, "
                f"{self._value_table}.Rank, "
                f"{self._value_table}.Value "
                f"FROM {self._value_table} "
                f"JOIN {self._game_table} "
                f"ON {self._game_table}.UUID = {self._value_table}.GameID "
                f"JOIN {self._season_table} "
                f"ON {self._season_table}.UUID = {self._game_table}.SeasonID "
                f"JOIN {self._team_table} home_team "
                f"ON home_team.UUID = {self._game_table}.HomeTeamID "
                f"JOIN {self._team_table} away_team "
                f"ON away_team.UUID = {self._game_table}.AwayTeamID "
                f"WHERE {self._value_table}.RankingID = ?;",
                [row[0]],
            )
            values = [
                GameRankingValueBySeasonWeekResult(
                    UUID(value[0]),
                    UUID(value[1]),
                    value[2],
                    value[3],
                    datetime.strptime(value[4], "%Y-%m-%d").date(),
                    value[5],
                    UUID(value[6]),
                    value[7],
                    UUID(value[8]),
                    value[9],
                    value[10],
                    value[11],
                    value[12],
                    value[13],
                    value[14],
                    value[15],
                    value[16],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return GameRankingBySeasonWeekResult(
                UUID(row[0]),
                row[1],
                UUID(row[2]),
                row[3],
                row[4],
                values,
            )
        return None

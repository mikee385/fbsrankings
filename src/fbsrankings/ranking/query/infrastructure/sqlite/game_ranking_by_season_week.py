import sqlite3
from datetime import datetime
from typing import Union

from fbsrankings.messages.convert import datetime_to_timestamp
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingBySeasonWeekValue
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
    ) -> GameRankingBySeasonWeekResult:
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

        params: list[SqliteParam] = [
            query.name,
            RankingType.GAME.name,
            query.season_id,
        ]

        if query.HasField("week"):
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
                    game_id=value[0],
                    season_id=value[1],
                    year=value[2],
                    week=value[3],
                    date=datetime_to_timestamp(datetime.strptime(value[4], "%Y-%m-%d")),
                    season_section=value[5],
                    home_team_id=value[6],
                    home_team_name=value[7],
                    away_team_id=value[8],
                    away_team_name=value[9],
                    home_team_score=value[10],
                    away_team_score=value[11],
                    status=value[12],
                    notes=value[13],
                    order=value[14],
                    rank=value[15],
                    value=value[16],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return GameRankingBySeasonWeekResult(
                query_id=query.query_id,
                ranking=GameRankingBySeasonWeekValue(
                    ranking_id=row[0],
                    name=row[1],
                    season_id=row[2],
                    year=row[3],
                    week=row[4],
                    values=values,
                ),
            )

        return GameRankingBySeasonWeekResult(query_id=query.query_id, ranking=None)

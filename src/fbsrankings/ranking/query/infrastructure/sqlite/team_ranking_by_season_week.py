import sqlite3
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from fbsrankings.shared.query import TeamRankingBySeasonWeekQuery
from fbsrankings.shared.query import TeamRankingBySeasonWeekResult
from fbsrankings.shared.query import TeamRankingValueBySeasonWeekResult
from fbsrankings.storage.sqlite import RankingTable
from fbsrankings.storage.sqlite import RankingType
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamRankingValueTable
from fbsrankings.storage.sqlite import TeamTable


SqliteParam = Union[None, int, float, str, bytes]


class TeamRankingBySeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._ranking_table = RankingTable().table
        self._value_table = TeamRankingValueTable().table
        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table

    def __call__(
        self,
        query: TeamRankingBySeasonWeekQuery,
    ) -> Optional[TeamRankingBySeasonWeekResult]:
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
            RankingType.TEAM.name,
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
                f"{self._value_table}.TeamID, "
                f"{self._team_table}.Name, "
                f"{self._value_table}.Ord, "
                f"{self._value_table}.Rank, "
                f"{self._value_table}.Value "
                f"FROM {self._value_table} "
                f"JOIN {self._team_table} "
                f"ON {self._team_table}.UUID = {self._value_table}.TeamID "
                f"WHERE {self._value_table}.RankingID = ?;",
                [row[0]],
            )
            values = [
                TeamRankingValueBySeasonWeekResult(
                    UUID(value[0]),
                    value[1],
                    value[2],
                    value[3],
                    value[4],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return TeamRankingBySeasonWeekResult(
                UUID(row[0]),
                row[1],
                UUID(row[2]),
                row[3],
                row[4],
                values,
            )
        return None

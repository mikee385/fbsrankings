import sqlite3
from typing import Union

from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekResult
from fbsrankings.messages.query import TeamRecordBySeasonWeekValue
from fbsrankings.messages.query import TeamRecordValueBySeasonWeekResult
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamRecordTable
from fbsrankings.storage.sqlite import TeamRecordValueTable
from fbsrankings.storage.sqlite import TeamTable


SqliteParam = Union[None, int, float, str, bytes]


class TeamRecordBySeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._record_table = TeamRecordTable().table
        self._value_table = TeamRecordValueTable().table
        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table

    def __call__(
        self,
        query: TeamRecordBySeasonWeekQuery,
    ) -> TeamRecordBySeasonWeekResult:
        sql_query = (
            "SELECT "
            f"{self._record_table}.UUID, "
            f"{self._record_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"{self._record_table}.Week "
            f"FROM {self._record_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._record_table}.SeasonID "
            f"WHERE {self._record_table}.SeasonID = ?"
        )

        params: list[SqliteParam] = [
            query.season_id,
        ]

        if query.HasField("week"):
            sql_query += f" AND {self._record_table}.Week = ?;"
            params.append(query.week)
        else:
            sql_query += f" AND {self._record_table}.Week IS NULL;"
        cursor = self._connection.cursor()
        cursor.execute(sql_query, params)
        row = cursor.fetchone()

        values = []
        if row is not None:
            cursor.execute(
                "SELECT "
                f"{self._value_table}.TeamID, "
                f"{self._team_table}.Name, "
                f"{self._value_table}.Wins, "
                f"{self._value_table}.Losses "
                f"FROM {self._value_table} "
                f"JOIN {self._team_table} "
                f"ON {self._team_table}.UUID = {self._value_table}.TeamID "
                f"WHERE {self._value_table}.TeamRecordID = ?;",
                [row[0]],
            )
            values = [
                TeamRecordValueBySeasonWeekResult(
                    team_id=value[0],
                    name=value[1],
                    wins=value[2],
                    losses=value[3],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return TeamRecordBySeasonWeekResult(
                query_id=query.query_id,
                record=TeamRecordBySeasonWeekValue(
                    record_id=row[0],
                    season_id=row[1],
                    year=row[2],
                    week=row[3],
                    values=values,
                ),
            )

        return TeamRecordBySeasonWeekResult(query_id=query.query_id, record=None)

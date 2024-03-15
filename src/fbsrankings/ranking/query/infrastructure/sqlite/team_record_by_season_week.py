import sqlite3
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.ranking.query.query.team_record_by_season_week import (
    TeamRecordBySeasonWeekQuery,
)
from fbsrankings.ranking.query.query.team_record_by_season_week import (
    TeamRecordBySeasonWeekResult,
)
from fbsrankings.ranking.query.query.team_record_by_season_week import (
    TeamRecordValueBySeasonWeekResult,
)
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
    ) -> Optional[TeamRecordBySeasonWeekResult]:
        sql_query = (
            Query.from_(self._record_table)
            .select(
                self._record_table.UUID,
                self._record_table.SeasonID,
                self._season_table.Year,
                self._record_table.Week,
            )
            .inner_join(self._season_table)
            .on(self._season_table.UUID == self._record_table.SeasonID)
            .where(self._record_table.SeasonID == Parameter("?"))
        )

        params: List[SqliteParam] = [
            str(query.season_id),
        ]

        if query.week is not None:
            sql_query = sql_query.where(self._record_table.Week == Parameter("?"))
            params.append(query.week)
        else:
            sql_query = sql_query.where(self._record_table.Week.isnull())

        cursor = self._connection.cursor()
        cursor.execute(sql_query.get_sql(), params)
        row = cursor.fetchone()

        values = []
        if row is not None:
            cursor.execute(
                Query.from_(self._value_table)
                .select(
                    self._value_table.TeamID,
                    self._team_table.Name,
                    self._value_table.Wins,
                    self._value_table.Losses,
                )
                .inner_join(self._team_table)
                .on(self._team_table.UUID == self._value_table.TeamID)
                .where(self._value_table.TeamRecordID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )
            values = [
                TeamRecordValueBySeasonWeekResult(
                    UUID(value[0]),
                    value[1],
                    value[2],
                    value[3],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return TeamRecordBySeasonWeekResult(
                UUID(row[0]),
                UUID(row[1]),
                row[2],
                row[3],
                values,
            )
        return None

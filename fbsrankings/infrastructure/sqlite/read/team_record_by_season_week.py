import sqlite3
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.infrastructure.sqlite.storage import TeamRecordTable
from fbsrankings.infrastructure.sqlite.storage import TeamRecordValueTable
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekResult
from fbsrankings.query import TeamRecordValueBySeasonWeekResult


SqliteParam = Union[None, int, float, str, bytes]


class TeamRecordBySeasonWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.record_table = TeamRecordTable()
        self.value_table = TeamRecordValueTable()
        self.season_table = SeasonTable()
        self.team_table = TeamTable()

    def __call__(
        self, query: TeamRecordBySeasonWeekQuery
    ) -> Optional[TeamRecordBySeasonWeekResult]:
        where = "record.SeasonID=?"
        params: List[SqliteParam] = [
            str(query.season_ID),
        ]

        if query.week is not None:
            where += " AND Week=?"
            params.append(query.week)
        else:
            where += " AND Week is NULL"

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT record.UUID, record.SeasonID, season.Year, record.Week FROM {self.record_table.name} AS record INNER JOIN {self.season_table.name} AS season ON season.UUID = record.SeasonID WHERE {where}",
            params,
        )
        row = cursor.fetchone()

        values = []
        if row is not None:
            cursor.execute(
                f"SELECT value.TeamID, team.Name, value.Wins, value.Losses FROM {self.value_table.name} AS value INNER JOIN {self.team_table.name} AS team ON team.UUID = value.TeamID WHERE value.TeamRecordID=?",
                [row[0]],
            )
            values = [
                TeamRecordValueBySeasonWeekResult(
                    UUID(value[0]), value[1], value[2], value[3]
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return TeamRecordBySeasonWeekResult(
                UUID(row[0]), UUID(row[1]), row[2], row[3], values
            )
        else:
            return None

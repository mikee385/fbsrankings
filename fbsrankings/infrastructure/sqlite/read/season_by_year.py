import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonByYearResult


class SeasonByYearQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = SeasonTable()

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self.table.name} WHERE Year=?", [str(query.year)]
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByYearResult(UUID(row[0]), row[1])
        else:
            return None

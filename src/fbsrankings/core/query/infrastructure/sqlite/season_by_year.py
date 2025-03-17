import sqlite3
from typing import Optional

from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.storage.sqlite import SeasonTable


class SeasonByYearQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self._table} WHERE Year = ?;",
            [query.year],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByYearResult(season_id=row[0], year=row[1])
        return None

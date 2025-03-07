import sqlite3
from typing import Optional

from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.storage.sqlite import SeasonTable


class SeasonByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self._table} WHERE UUID = ?;",
            [query.season_id],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByIDResult(row[0], row[1])
        return None

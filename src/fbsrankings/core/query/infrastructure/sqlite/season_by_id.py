import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.shared.query import SeasonByIDQuery
from fbsrankings.shared.query import SeasonByIDResult
from fbsrankings.storage.sqlite import SeasonTable


class SeasonByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self._table} WHERE UUID = ?;",
            [str(query.id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByIDResult(UUID(row[0]), row[1])
        return None

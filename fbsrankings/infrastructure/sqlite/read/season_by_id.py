import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByIDResult


class SeasonByIDQueryHandler(QueryHandler[SeasonByIDQuery, Optional[SeasonByIDResult]]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = SeasonTable()

    def handle(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self.table.name} WHERE UUID=?", [str(query.ID)]
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByIDResult(UUID(row[0]), row[1])
        else:
            return None

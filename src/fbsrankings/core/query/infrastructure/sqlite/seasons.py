import sqlite3
from uuid import UUID

from pypika import Query

from fbsrankings.core.query.query.seasons import SeasonResult
from fbsrankings.core.query.query.seasons import SeasonsQuery
from fbsrankings.core.query.query.seasons import SeasonsResult
from fbsrankings.storage.sqlite import SeasonTable


class SeasonsQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(self._table.UUID, self._table.Year)
            .get_sql(),
        )
        items = [SeasonResult(UUID(row[0]), row[1]) for row in cursor.fetchall()]
        cursor.close()

        return SeasonsResult(items)

import sqlite3
from typing import Optional
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonByYearResult


class SeasonByYearQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(self._table.UUID, self._table.Year)
            .where(self._table.Year == Parameter("?"))
            .get_sql(),
            [str(query.year)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByYearResult(UUID(row[0]), row[1])
        return None

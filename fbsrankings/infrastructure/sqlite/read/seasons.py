import sqlite3
from uuid import UUID

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.query import SeasonResult
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import SeasonsResult


class SeasonsQueryHandler(QueryHandler[SeasonsQuery, SeasonsResult]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = SeasonTable()

    def handle(self, query: SeasonsQuery) -> SeasonsResult:
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT UUID, Year FROM {self.table.name}")
        items = [SeasonResult(UUID(row[0]), row[1]) for row in cursor.fetchall()]
        cursor.close()

        return SeasonsResult(items)

import sqlite3

from uuid import UUID

from fbsrankings.common import Query, QueryHandler
from fbsrankings.query import SeasonsQuery, SeasonsResult, SeasonResult
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonsQueryHandler (QueryHandler):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        
        self.table = SeasonTable()
        
    def handle(self, query: Query) -> SeasonsResult:
        if not isinstance(query, SeasonsQuery):
            raise TypeError('query must be of type SeasonsQuery')

        cursor = self._connection.cursor()
        cursor.execute(f'SELECT UUID, Year FROM {self.table.name}')
        items = [SeasonResult(UUID(row[0]), row[1]) for row in cursor.fetchall()]
        cursor.close()
        
        return SeasonsResult(items)

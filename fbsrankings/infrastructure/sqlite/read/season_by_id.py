import sqlite3

from typing import Optional
from uuid import UUID

from fbsrankings.common import Query, QueryHandler
from fbsrankings.query import SeasonByIDQuery, SeasonByIDResult
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonByIDQueryHandler (QueryHandler):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        
        self.table = SeasonTable()
        
    def handle(self, query: Query) -> Optional[SeasonByIDResult]:
        if not isinstance(query, SeasonByIDQuery):
            raise TypeError('query must be of type SeasonByIDQuery')

        cursor = self._connection.cursor()
        cursor.execute(f'SELECT UUID, Year FROM {self.table.name} WHERE UUID=?', [str(query.ID)])
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return SeasonByIDResult(UUID(row[0]), row[1])
        else:
            return None

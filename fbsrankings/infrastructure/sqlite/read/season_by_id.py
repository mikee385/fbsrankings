import sqlite3
from uuid import UUID

from fbsrankings.query import SeasonByIDResult
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonByIDQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = SeasonTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT UUID, Year FROM {self.table.name} WHERE UUID=?', [str(query.ID)])
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return SeasonByIDResult(UUID(row[0]), row[1])
        else:
            return None

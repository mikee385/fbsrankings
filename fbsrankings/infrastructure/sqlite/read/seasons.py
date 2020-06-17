import sqlite3
from uuid import UUID

from fbsrankings.query import SeasonsResult, SeasonResult
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonsQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = SeasonTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT UUID, Year FROM {self.table.name}')
        items = [SeasonResult(UUID(row[0]), row[1]) for row in cursor.fetchall()]
        cursor.close()
        
        return SeasonsResult(items)

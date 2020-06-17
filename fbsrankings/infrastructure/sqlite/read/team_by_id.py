import sqlite3
from uuid import UUID

from fbsrankings.query import TeamByIDResult
from fbsrankings.infrastructure.sqlite.storage import TeamTable


class TeamByIDQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = TeamTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT UUID, Name FROM {self.table.name} WHERE UUID=?', [str(query.ID)])
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return TeamByIDResult(UUID(row[0]), row[1])
        else:
            return None

import sqlite3

from fbsrankings.query import GameCountBySeasonResult
from fbsrankings.infrastructure.sqlite.storage import GameTable


class GameCountBySeasonQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = GameTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?', [str(query.season_ID)])
        row = cursor.fetchone()
        cursor.close()
        
        return GameCountBySeasonResult(query.season_ID, row[0])

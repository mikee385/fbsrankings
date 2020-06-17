import sqlite3

from fbsrankings.query import TeamCountBySeasonResult
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable


class TeamCountBySeasonQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = AffiliationTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?', [str(query.season_ID)])
        row = cursor.fetchone()
        cursor.close()
        
        return TeamCountBySeasonResult(query.season_ID, row[0])

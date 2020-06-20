import sqlite3

from fbsrankings.common import Query, QueryHandler
from fbsrankings.query import GameCountBySeasonQuery, GameCountBySeasonResult
from fbsrankings.infrastructure.sqlite.storage import GameTable


class GameCountBySeasonQueryHandler (QueryHandler):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        
        self.table = GameTable()
        
    def handle(self, query: Query) -> GameCountBySeasonResult:
        if not isinstance(query, GameCountBySeasonQuery):
            raise TypeError('query must be of type GameCountBySeasonQuery')

        cursor = self._connection.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?', [str(query.season_ID)])
        row = cursor.fetchone()
        cursor.close()
        
        return GameCountBySeasonResult(query.season_ID, row[0])

import sqlite3

from fbsrankings.common import Query, QueryHandler
from fbsrankings.query import TeamCountBySeasonQuery, TeamCountBySeasonResult
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable


class TeamCountBySeasonQueryHandler (QueryHandler):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        
        self.table = AffiliationTable()
        
    def handle(self, query: Query) -> TeamCountBySeasonResult:
        if not isinstance(query, TeamCountBySeasonQuery):
            raise TypeError('query must be of type TeamCountBySeasonQuery')

        cursor = self._connection.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?', [str(query.season_ID)])
        row = cursor.fetchone()
        cursor.close()
        
        return TeamCountBySeasonResult(query.season_ID, row[0])

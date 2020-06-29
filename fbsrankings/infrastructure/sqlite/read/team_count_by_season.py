import sqlite3

from fbsrankings.infrastructure.sqlite.storage import AffiliationTable
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamCountBySeasonResult


class TeamCountBySeasonQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = AffiliationTable()

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?",
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return TeamCountBySeasonResult(query.season_ID, row[0])

import sqlite3

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable
from fbsrankings.query import TeamCountBySeasonQuery, TeamCountBySeasonResult


class TeamCountBySeasonQueryHandler(
    QueryHandler[TeamCountBySeasonQuery, TeamCountBySeasonResult]
):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = AffiliationTable()

    def handle(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?",
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return TeamCountBySeasonResult(query.season_ID, row[0])

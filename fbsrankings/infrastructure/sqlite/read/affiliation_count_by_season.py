import sqlite3

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import AffiliationCountBySeasonResult


class AffiliationCountBySeasonQueryHandler(
    QueryHandler[AffiliationCountBySeasonQuery, AffiliationCountBySeasonResult]
):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = AffiliationTable()

    def handle(
        self, query: AffiliationCountBySeasonQuery
    ) -> AffiliationCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f'SELECT SUM(CASE WHEN Subdivision = "FBS" THEN 1 ELSE 0 END) AS FBS_Count, SUM(CASE WHEN Subdivision = "FCS" THEN 1 ELSE 0 END) AS FCS_Count FROM {self.table.name} WHERE SeasonID=?',
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return AffiliationCountBySeasonResult(query.season_ID, row[0], row[1])

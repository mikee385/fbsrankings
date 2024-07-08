import sqlite3

from fbsrankings.shared.enums import Subdivision
from fbsrankings.shared.query import AffiliationCountBySeasonQuery
from fbsrankings.shared.query import AffiliationCountBySeasonResult
from fbsrankings.storage.sqlite import AffiliationTable


class AffiliationCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = AffiliationTable().table

    def __call__(
        self,
        query: AffiliationCountBySeasonQuery,
    ) -> AffiliationCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            "SUM(CASE WHEN Subdivision = ? THEN 1 ELSE 0 END) FBS_Count, "
            "SUM(CASE WHEN Subdivision = ? THEN 1 ELSE 0 END) FCS_Count "
            f"FROM {self._table} "
            "WHERE SeasonID = ?;",
            [Subdivision.FBS.name, Subdivision.FCS.name, str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return AffiliationCountBySeasonResult(query.season_id, row[0], row[1])

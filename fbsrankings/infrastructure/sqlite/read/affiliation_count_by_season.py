import sqlite3

from pypika import Case
from pypika import Parameter
from pypika import Query
from pypika.functions import Sum

from fbsrankings.infrastructure.sqlite.storage import AffiliationTable
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import AffiliationCountBySeasonResult


class AffiliationCountBySeasonQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = AffiliationTable().table

    def __call__(
        self, query: AffiliationCountBySeasonQuery
    ) -> AffiliationCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(
                Sum(Case().when(self._table.Subdivision == "FBS", 1).else_(0)).as_(
                    "FBS_Count"
                ),
                Sum(Case().when(self._table.Subdivision == "FCS", 1).else_(0)).as_(
                    "FCS_Count"
                ),
            )
            .where(self._table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return AffiliationCountBySeasonResult(query.season_ID, row[0], row[1])

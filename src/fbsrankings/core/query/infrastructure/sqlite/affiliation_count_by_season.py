import sqlite3

from pypika import Case
from pypika import Parameter
from pypika import Query
from pypika.functions import Sum

from fbsrankings.core.query.query.affiliation_count_by_season import (
    AffiliationCountBySeasonQuery,
)
from fbsrankings.core.query.query.affiliation_count_by_season import (
    AffiliationCountBySeasonResult,
)
from fbsrankings.enums import Subdivision
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
            Query.from_(self._table)
            .select(
                Sum(
                    Case()
                    .when(self._table.Subdivision == Subdivision.FBS.name, 1)
                    .else_(0),
                ).as_(
                    "FBS_Count",
                ),
                Sum(
                    Case()
                    .when(self._table.Subdivision == Subdivision.FCS.name, 1)
                    .else_(0),
                ).as_(
                    "FCS_Count",
                ),
            )
            .where(self._table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return AffiliationCountBySeasonResult(query.season_id, row[0], row[1])

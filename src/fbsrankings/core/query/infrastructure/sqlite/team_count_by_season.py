import sqlite3

from pypika import Parameter
from pypika import Query
from pypika.functions import Count

from fbsrankings.core.query.query.team_count_by_season import TeamCountBySeasonQuery
from fbsrankings.core.query.query.team_count_by_season import TeamCountBySeasonResult
from fbsrankings.storage.sqlite import AffiliationTable


class TeamCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = AffiliationTable().table

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(Count(self._table.star))
            .where(self._table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return TeamCountBySeasonResult(query.season_id, row[0])

import sqlite3

from pypika import Parameter
from pypika import Query
from pypika.functions import Max

from fbsrankings.shared.query import WeekCountBySeasonQuery
from fbsrankings.shared.query import WeekCountBySeasonResult
from fbsrankings.storage.sqlite import GameTable


class WeekCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = GameTable().table

    def __call__(self, query: WeekCountBySeasonQuery) -> WeekCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(Max(self._table.Week))
            .where(self._table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return WeekCountBySeasonResult(query.season_id, row[0])

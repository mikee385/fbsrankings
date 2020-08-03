import sqlite3

from pypika import Parameter
from pypika import Query
from pypika.functions import Count

from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameCountBySeasonResult


class GameCountBySeasonQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = GameTable().table

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(Count(self._table.star))
            .where(self._table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return GameCountBySeasonResult(query.season_ID, row[0])

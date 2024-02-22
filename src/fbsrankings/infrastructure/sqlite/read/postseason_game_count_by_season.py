import sqlite3

from pypika import Parameter
from pypika import Query
from pypika.functions import Count

from fbsrankings.domain import SeasonSection
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.query import PostseasonGameCountBySeasonQuery
from fbsrankings.query import PostseasonGameCountBySeasonResult


class PostseasonGameCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = GameTable().table

    def __call__(
        self,
        query: PostseasonGameCountBySeasonQuery,
    ) -> PostseasonGameCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(Count(self._table.star))
            .where(
                (self._table.SeasonID == Parameter("?"))
                & (self._table.SeasonSection == Parameter("?")),
            )
            .get_sql(),
            [str(query.season_id), SeasonSection.POSTSEASON.name],
        )
        row = cursor.fetchone()
        cursor.close()

        return PostseasonGameCountBySeasonResult(query.season_id, row[0])

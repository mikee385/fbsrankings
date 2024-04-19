import sqlite3

from pypika import Parameter
from pypika import Query
from pypika.functions import Count

from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQuery,
)
from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonResult,
)
from fbsrankings.enums import SeasonSection
from fbsrankings.storage.sqlite import GameTable


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

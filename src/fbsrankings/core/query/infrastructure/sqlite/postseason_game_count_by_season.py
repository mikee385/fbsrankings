import sqlite3

from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.query import PostseasonGameCountBySeasonQuery
from fbsrankings.messages.query import PostseasonGameCountBySeasonResult
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
            "SELECT COUNT(*) "
            f"FROM {self._table} "
            "WHERE SeasonID = ? AND SeasonSection = ?;",
            [str(query.season_id), SeasonSection.POSTSEASON.name],
        )
        row = cursor.fetchone()
        cursor.close()

        return PostseasonGameCountBySeasonResult(query.season_id, row[0])

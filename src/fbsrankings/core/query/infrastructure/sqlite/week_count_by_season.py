import sqlite3

from fbsrankings.messages.query import WeekCountBySeasonQuery
from fbsrankings.messages.query import WeekCountBySeasonResult
from fbsrankings.storage.sqlite import GameTable


class WeekCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = GameTable().table

    def __call__(self, query: WeekCountBySeasonQuery) -> WeekCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT MAX(Week) FROM {self._table} WHERE SeasonID = ?;",
            [query.season_id],
        )
        row = cursor.fetchone()
        cursor.close()

        return WeekCountBySeasonResult(
            query_id=query.query_id,
            season_id=query.season_id,
            count=row[0],
        )

import sqlite3

from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.query import WeekCountBySeasonQuery
from fbsrankings.query import WeekCountBySeasonResult


class WeekCountBySeasonQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = GameTable()

    def __call__(self, query: WeekCountBySeasonQuery) -> WeekCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT MAX(Week) FROM {self.table.name} WHERE SeasonID=?",
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return WeekCountBySeasonResult(query.season_ID, row[0])

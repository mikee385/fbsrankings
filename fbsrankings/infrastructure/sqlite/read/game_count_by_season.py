import sqlite3

from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameCountBySeasonResult


class GameCountBySeasonQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = GameTable()

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?",
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return GameCountBySeasonResult(query.season_ID, row[0])

import sqlite3

from fbsrankings.messages.query import GameCountBySeasonQuery
from fbsrankings.messages.query import GameCountBySeasonResult
from fbsrankings.storage.sqlite import GameTable


class GameCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = GameTable().table

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self._table} WHERE SeasonID = ?;",
            [str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return GameCountBySeasonResult(query.season_id, row[0])

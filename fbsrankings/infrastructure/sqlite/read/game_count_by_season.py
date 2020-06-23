import sqlite3

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.query import GameCountBySeasonQuery, GameCountBySeasonResult


class GameCountBySeasonQueryHandler(QueryHandler[GameCountBySeasonQuery]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = GameTable()

    def handle(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self.table.name} WHERE SeasonID=?",
            [str(query.season_ID)],
        )
        row = cursor.fetchone()
        cursor.close()

        return GameCountBySeasonResult(query.season_ID, row[0])

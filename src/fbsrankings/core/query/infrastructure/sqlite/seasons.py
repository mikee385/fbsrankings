import sqlite3

from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import SeasonsResult
from fbsrankings.storage.sqlite import SeasonTable


class SeasonsQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self._table};",
        )
        items = [
            SeasonResult(season_id=row[0], year=row[1]) for row in cursor.fetchall()
        ]
        cursor.close()

        return SeasonsResult(query_id=query.query_id, seasons=items)

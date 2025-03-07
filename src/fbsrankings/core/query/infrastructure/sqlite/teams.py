import sqlite3

from fbsrankings.messages.query import TeamResult
from fbsrankings.messages.query import TeamsQuery
from fbsrankings.messages.query import TeamsResult
from fbsrankings.storage.sqlite import TeamTable


class TeamsQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = TeamTable().table

    def __call__(self, query: TeamsQuery) -> TeamsResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Name FROM {self._table};",
        )
        items = [TeamResult(row[0], row[1]) for row in cursor.fetchall()]
        cursor.close()

        return TeamsResult(items)

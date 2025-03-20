import sqlite3

from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.messages.query import SeasonByIDValue
from fbsrankings.storage.sqlite import SeasonTable


class SeasonByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = SeasonTable().table

    def __call__(self, query: SeasonByIDQuery) -> SeasonByIDResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Year FROM {self._table} WHERE UUID = ?;",
            [query.season_id],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return SeasonByIDResult(
                query_id=query.query_id,
                season=SeasonByIDValue(season_id=row[0], year=row[1]),
            )
        return SeasonByIDResult(query_id=query.query_id, season=None)

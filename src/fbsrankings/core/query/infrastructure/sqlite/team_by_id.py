import sqlite3

from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamByIDResult
from fbsrankings.messages.query import TeamByIDValue
from fbsrankings.storage.sqlite import TeamTable


class TeamByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = TeamTable().table

    def __call__(self, query: TeamByIDQuery) -> TeamByIDResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Name FROM {self._table} WHERE UUID = ?;",
            [query.team_id],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return TeamByIDResult(
                query_id=query.query_id,
                team=TeamByIDValue(team_id=row[0], name=row[1]),
            )
        return TeamByIDResult(query_id=query.query_id, team=None)

import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.shared.query import TeamByIDQuery
from fbsrankings.shared.query import TeamByIDResult
from fbsrankings.storage.sqlite import TeamTable


class TeamByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = TeamTable().table

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT UUID, Name "
            f"FROM {self._table} "
            "WHERE UUID = ?;",
            [str(query.id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return TeamByIDResult(UUID(row[0]), row[1])
        return None

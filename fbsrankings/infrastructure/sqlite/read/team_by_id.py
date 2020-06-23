import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamByIDQuery, TeamByIDResult


class TeamByIDQueryHandler(QueryHandler):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = TeamTable()

    def handle(self, query: Query) -> Optional[TeamByIDResult]:
        if not isinstance(query, TeamByIDQuery):
            raise TypeError("query must be of type TeamByIDQuery")

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT UUID, Name FROM {self.table.name} WHERE UUID=?", [str(query.ID)]
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return TeamByIDResult(UUID(row[0]), row[1])
        else:
            return None

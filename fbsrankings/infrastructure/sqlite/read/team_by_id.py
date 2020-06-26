import sqlite3
from typing import Optional
from uuid import UUID

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamByIDResult


class TeamByIDQueryHandler(QueryHandler[TeamByIDQuery, Optional[TeamByIDResult]]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.table = TeamTable()

    def handle(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
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

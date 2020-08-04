import sqlite3
from typing import Optional
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamByIDResult


class TeamByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = TeamTable().table

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._table)
            .select(self._table.UUID, self._table.Name)
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [str(query.id)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return TeamByIDResult(UUID(row[0]), row[1])
        return None

import sqlite3
from typing import Optional
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.core.query.query.team_by_id import TeamByIDQuery
from fbsrankings.core.query.query.team_by_id import TeamByIDResult
from fbsrankings.storage.sqlite import TeamTable


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
            [str(query.id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return TeamByIDResult(UUID(row[0]), row[1])
        return None

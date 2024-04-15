import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.core.command.event.team import TeamCreatedEvent
from fbsrankings.core.command.event.team import TeamEventHandler as BaseEventHandler
from fbsrankings.storage.sqlite import TeamTable


class TeamRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = TeamTable().table
        self._bus = bus

    def get(self, id_: TeamID) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.UUID == Parameter("?")).get_sql(),
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_team(row) if row is not None else None

    def find(self, name: str) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.Name == Parameter("?")).get_sql(),
            [name],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_team(row) if row is not None else None

    def _query(self) -> QueryBuilder:
        return Query.from_(self._table).select(self._table.UUID, self._table.Name)

    def _to_team(self, row: Tuple[str, str]) -> Team:
        return Team(self._bus, TeamID(UUID(row[0])), row[1])


class TeamEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._table = TeamTable().table

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._cursor.execute(
            Query.into(self._table)
            .columns(self._table.UUID, self._table.Name)
            .insert(Parameter("?"), Parameter("?"))
            .get_sql(),
            [str(event.id_), event.name],
        )

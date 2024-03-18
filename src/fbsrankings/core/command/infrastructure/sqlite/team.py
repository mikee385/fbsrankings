import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import (
    TeamEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.core.command.event.team import TeamCreatedEvent
from fbsrankings.storage.sqlite import Storage
from fbsrankings.storage.sqlite import TeamTable


class TeamRepository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        super().__init__(bus)
        self._cache = storage.cache
        self._connection = storage.connection
        self._table = TeamTable().table

    def get(self, id_: TeamID) -> Optional[Team]:
        key = f"team:{id_}"
        row = self._cache.get(key)
        if row is None:
            cursor = self._connection.cursor()
            cursor.execute(
                self._query().where(self._table.UUID == Parameter("?")).get_sql(),
                [str(id_.value)],
            )
            row = cursor.fetchone()
            cursor.close()
        if row is not None:
            self._cache[key] = row

        return self._to_team(row) if row is not None else None

    def find(self, name: str) -> Optional[Team]:
        key = f"team:{name}"
        row = self._cache.get(key)
        if row is None:
            cursor = self._connection.cursor()
            cursor.execute(
                self._query().where(self._table.Name == Parameter("?")).get_sql(),
                [name],
            )
            row = cursor.fetchone()
            cursor.close()
        if row is not None:
            self._cache[key] = row

        return self._to_team(row) if row is not None else None

    def _query(self) -> QueryBuilder:
        return Query.from_(self._table).select(self._table.UUID, self._table.Name)

    def _to_team(self, row: Tuple[str, str]) -> Team:
        return Team(self._bus, TeamID(UUID(row[0])), row[1])


class TeamEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor, bus: EventBus) -> None:
        super().__init__(bus)
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

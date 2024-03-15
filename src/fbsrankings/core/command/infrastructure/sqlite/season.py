import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import (
    SeasonEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.season import (
    SeasonRepository as BaseRepository,
)
from fbsrankings.core.command.event.season import SeasonCreatedEvent
from fbsrankings.storage.sqlite import SeasonTable


class SeasonRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        super().__init__(bus)
        self._connection = connection
        self._table = SeasonTable().table

    def get(self, id_: SeasonID) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.UUID == Parameter("?")).get_sql(),
            [str(id_.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def find(self, year: int) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.Year == Parameter("?")).get_sql(),
            [year],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def _query(self) -> QueryBuilder:
        return Query.from_(self._table).select(self._table.UUID, self._table.Year)

    def _to_season(self, row: Tuple[str, int]) -> Season:
        return Season(self._bus, SeasonID(UUID(row[0])), row[1])


class SeasonEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor, bus: EventBus) -> None:
        super().__init__(bus)
        self._cursor = cursor
        self._table = SeasonTable().table

    def handle_created(self, event: SeasonCreatedEvent) -> None:
        self._cursor.execute(
            Query.into(self._table)
            .columns(self._table.UUID, self._table.Year)
            .insert(Parameter("?"), Parameter("?"))
            .get_sql(),
            [str(event.id_), event.year],
        )

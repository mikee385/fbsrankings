import sqlite3
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.common import EventBus
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonRepository(BaseRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self._table = SeasonTable().table

        bus.register_handler(SeasonCreatedEvent, self._handle_season_created)

    def get(self, ID: SeasonID) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def find(self, year: int) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .where(self._table.Year == Parameter("?"))
            .get_sql(),
            [year]
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def all(self) -> List[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .get_sql()
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_season(row) for row in rows if row is not None]

    def _query(self) -> Query:
        return Query.from_(self._table).select(
            self._table.UUID,
            self._table.Year
        )

    def _to_season(self, row: Tuple[str, int]) -> Season:
        return Season(self._bus, SeasonID(UUID(row[0])), row[1])

    def _handle_season_created(self, event: SeasonCreatedEvent) -> None:
        self._cursor.execute(
            Query.into(self._table)
            .columns(
                self._table.UUID,
                self._table.Year
            )
            .insert(
                Parameter("?"),
                Parameter("?")
            )
            .get_sql(),
            [
                str(event.ID),
                event.year
            ],
        )

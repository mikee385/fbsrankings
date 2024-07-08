import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.season import (
    SeasonRepository as BaseRepository,
)
from fbsrankings.shared.event import SeasonCreatedEvent
from fbsrankings.shared.event import SeasonEventHandler as BaseEventHandler
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.sqlite import SeasonTable


class SeasonRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = SeasonTable().table
        self._bus = bus

    def get(self, id_: SeasonID) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ?;",
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def find(self, year: int) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE Year = ?;",
            [year],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_season(row) if row is not None else None

    def _query(self) -> str:
        return f"SELECT UUID, Year FROM {self._table}"

    def _to_season(self, row: Tuple[str, int]) -> Season:
        return Season(self._bus, SeasonID(UUID(row[0])), row[1])


class SeasonEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._table = SeasonTable().table

    def handle_created(self, event: SeasonCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self._table} (UUID, Year) VALUES (?,?);",
            [str(event.id_), event.year],
        )

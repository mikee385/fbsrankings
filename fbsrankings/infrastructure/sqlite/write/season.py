import sqlite3
from typing import Optional, Tuple
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID
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

        self.table = SeasonTable()

        bus.register_handler(SeasonCreatedEvent, self._handle_season_created)

    def get(self, ID: SeasonID) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?",
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()
        return self._to_season(row)

    def find(self, year: int) -> Optional[Season]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE Year=?", [year]
        )
        row = cursor.fetchone()
        cursor.close()
        return self._to_season(row)

    def _to_season(self, row: Tuple[str, int]) -> Optional[Season]:
        if row is not None:
            return Season(self._bus, SeasonID(UUID(row[0])), row[1])
        else:
            return None

    def _handle_season_created(self, event: SeasonCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)",
            [str(event.ID), event.year],
        )

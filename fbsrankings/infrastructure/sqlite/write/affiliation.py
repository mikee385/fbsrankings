import sqlite3
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import SeasonID
from fbsrankings.domain import Subdivision
from fbsrankings.domain import TeamID
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable


class AffiliationRepository(BaseRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self.table = AffiliationTable()

        bus.register_handler(AffiliationCreatedEvent, self._handle_affiliation_created)

    def get(self, ID: AffiliationID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?",
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def find(self, season_ID: SeasonID, team_ID: TeamID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE SeasonID=? AND TeamID=?",
            [str(season_ID.value), str(team_ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def for_season(self, season_ID: SeasonID) -> List[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE SeasonID=?",
            [str(season_ID.value)],
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_affiliation(row) for row in rows if row is not None]

    def _to_affiliation(self, row: Tuple[str, str, str, str]) -> Affiliation:
        return Affiliation(
            self._bus,
            AffiliationID(UUID(row[0])),
            SeasonID(UUID(row[1])),
            TeamID(UUID(row[2])),
            Subdivision[row[3]],
        )

    def _handle_affiliation_created(self, event: AffiliationCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?)",
            [
                str(event.ID),
                str(event.season_ID),
                str(event.team_ID),
                event.subdivision,
            ],
        )

import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.affiliation import AffiliationID
from fbsrankings.core.command.domain.model.affiliation import (
    AffiliationRepository as BaseRepository,
)
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.messages.enums import Subdivision
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.event import AffiliationEventHandler as BaseEventHandler
from fbsrankings.storage.sqlite import AffiliationTable


class AffiliationRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = AffiliationTable().table
        self._bus = bus

    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ?;",
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE SeasonID = ? AND TeamID = ?;",
            [str(season_id), str(team_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def _query(self) -> str:
        return (
            "SELECT "
            "UUID, "
            "SeasonID, "
            "TeamID, "
            "Subdivision "
            f"FROM {self._table}"
        )

    def _to_affiliation(self, row: Tuple[str, str, str, str]) -> Affiliation:
        return Affiliation(
            self._bus,
            AffiliationID(UUID(row[0])),
            SeasonID(UUID(row[1])),
            TeamID(UUID(row[2])),
            Subdivision[row[3]],
        )


class AffiliationEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._table = AffiliationTable().table

    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self._table} "
            "(UUID, SeasonID, TeamID, Subdivision) "
            "VALUES (?,?,?,?);",
            [
                str(event.affiliation_id),
                str(event.season_id),
                str(event.team_id),
                event.subdivision,
            ],
        )

import sqlite3
from typing import Any, Optional, Union
from uuid import UUID

from fbsrankings.common import Event, EventBus
from fbsrankings.domain import Affiliation, AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import Season, SeasonID, Subdivision, Team, TeamID
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
        return self._to_affiliation(row)

    def find(
        self, season: Union[Season, SeasonID], team: Union[Team, TeamID]
    ) -> Optional[Affiliation]:
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError("season must be of type Season or SeasonID")

        if isinstance(team, Team):
            team_ID = team.ID
        elif isinstance(team, TeamID):
            team_ID = team
        else:
            raise TypeError("team must be of type Team or TeamID")

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=? AND TeamID=?",
            [str(season_ID.value), str(team_ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()
        return self._to_affiliation(row)

    def _to_affiliation(self, row: Any) -> Optional[Affiliation]:
        if row is not None:
            return Affiliation(
                self._bus,
                AffiliationID(UUID(row[0])),
                SeasonID(UUID(row[1])),
                TeamID(UUID(row[2])),
                Subdivision[row[3]],
            )
        else:
            return None

    def _handle_affiliation_created(self, event: Event) -> None:
        if not isinstance(event, AffiliationCreatedEvent):
            raise TypeError("event must be of type AffiliationCreatedEvent")

        self._cursor.execute(
            f"INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?)",
            [
                str(event.ID),
                str(event.season_ID),
                str(event.team_ID),
                event.subdivision,
            ],
        )

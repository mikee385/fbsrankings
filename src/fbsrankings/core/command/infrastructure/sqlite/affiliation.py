import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.affiliation import AffiliationID
from fbsrankings.core.command.domain.model.affiliation import (
    AffiliationRepository as BaseRepository,
)
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.shared.enums import Subdivision
from fbsrankings.shared.event import AffiliationCreatedEvent
from fbsrankings.shared.event import AffiliationEventHandler as BaseEventHandler
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.sqlite import AffiliationTable


class AffiliationRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = AffiliationTable().table
        self._bus = bus

    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.UUID == Parameter("?")).get_sql(),
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .where(self._table.SeasonID == Parameter("?"))
            .where(self._table.TeamID == Parameter("?"))
            .get_sql(),
            [str(season_id), str(team_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_affiliation(row) if row is not None else None

    def _query(self) -> QueryBuilder:
        return Query.from_(self._table).select(
            self._table.UUID,
            self._table.SeasonID,
            self._table.TeamID,
            self._table.Subdivision,
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
            Query.into(self._table)
            .columns(
                self._table.UUID,
                self._table.SeasonID,
                self._table.TeamID,
                self._table.Subdivision,
            )
            .insert(Parameter("?"), Parameter("?"), Parameter("?"), Parameter("?"))
            .get_sql(),
            [
                str(event.id_),
                str(event.season_id),
                str(event.team_id),
                event.subdivision,
            ],
        )

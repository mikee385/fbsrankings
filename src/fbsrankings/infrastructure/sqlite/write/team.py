import sqlite3
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Tuple
from typing import Type
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder
from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.sqlite.storage import TeamTable


class TeamRepository(BaseRepository, ContextManager["TeamRepository"]):
    def __init__(
        self,
        connection: sqlite3.Connection,
        cursor: sqlite3.Cursor,
        bus: EventBus,
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self._table = TeamTable().table

        self._bus.register_handler(TeamCreatedEvent, self._handle_team_created)

    def close(self) -> None:
        self._bus.unregister_handler(TeamCreatedEvent, self._handle_team_created)

    def get(self, id_: TeamID) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.UUID == Parameter("?")).get_sql(),
            [str(id_.value)],
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

    def _handle_team_created(self, event: TeamCreatedEvent) -> None:
        self._cursor.execute(
            Query.into(self._table)
            .columns(self._table.UUID, self._table.Name)
            .insert(Parameter("?"), Parameter("?"))
            .get_sql(),
            [str(event.id_), event.name],
        )

    def __enter__(self) -> "TeamRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

import sqlite3
from typing import Optional
from typing import Tuple
from uuid import UUID

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.messages.event import TeamCreatedEvent
from fbsrankings.messages.event import TeamEventHandler as BaseEventHandler
from fbsrankings.storage.sqlite import TeamTable


class TeamRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = TeamTable().table
        self._bus = bus

    def get(self, id_: TeamID) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ?;",
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_team(row) if row is not None else None

    def find(self, name: str) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE Name = ?;",
            [name],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_team(row) if row is not None else None

    def _query(self) -> str:
        return f"SELECT UUID, Name FROM {self._table}"

    def _to_team(self, row: Tuple[str, str]) -> Team:
        return Team(self._bus, TeamID(UUID(row[0])), row[1])


class TeamEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._table = TeamTable().table

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self._table} (UUID, Name) VALUES (?,?);",
            [str(event.team_id), event.name],
        )

import sqlite3

from typing import Any, Optional
from uuid import UUID

from fbsrankings.common import Event, EventBus
from fbsrankings.domain import Team, TeamID, TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.sqlite.storage import TeamTable


class TeamRepository (BaseRepository):
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus) -> None:
        super().__init__(bus)
        
        self._connection = connection
        self._cursor = cursor
        
        self.table = TeamTable()
        
        bus.register_handler(TeamCreatedEvent, self._handle_team_created)

    def get(self, ID: TeamID) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._to_team(row)
        
    def find(self, name: str) -> Optional[Team]:
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE Name=?', [name])
        row = cursor.fetchone()
        cursor.close()
        return self._to_team(row)
    
    def _to_team(self, row: Any) -> Optional[Team]:
        if row is not None:
            return Team(self._bus, TeamID(UUID(row[0])), row[1])
        else:
            return None

    def _handle_team_created(self, event: Event) -> None:
        if not isinstance(event, TeamCreatedEvent):
            raise TypeError('event must be of type TeamCreatedEvent')

        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)', [str(event.ID), event.name])

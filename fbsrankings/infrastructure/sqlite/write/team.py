import sqlite3
from uuid import UUID

from fbsrankings.domain import Team, TeamID, TeamRepository as BaseRepository
from fbsrankings.event import TeamRegisteredEvent
from fbsrankings.infrastructure.sqlite.storage import TeamTable


class TeamRepository (BaseRepository):
    def __init__(self, connection, cursor, bus):
        super().__init__(bus)
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        self.table = TeamTable()
        
        bus.register_handler(TeamRegisteredEvent, self._handle_team_registered)

    def find_by_ID(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._team_from_row(row)
        
    def find_by_name(self, name):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE Name=?', [name])
        row = cursor.fetchone()
        cursor.close()
        return self._team_from_row(row)
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}')
        items = [self._team_from_row(row) for row in cursor.fetchall()]
        cursor.close()
        return items
    
    def _team_from_row(self, row):
        if row is not None:
            return Team(self._bus, TeamID(UUID(row[0])), row[1])
        else:
            return None

    def _handle_team_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)', [str(event.ID.value), event.name])

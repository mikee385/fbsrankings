import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Team, TeamID, TeamRepository as BaseRepository, TeamRegisteredEvent


class TeamRepository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._table = 'team'
        self._columns = 'UUID, Name'
        
        cursor = self._connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (UUID TEXT NOT NULL UNIQUE,
             Name TEXT NOT NULL UNIQUE);''')
        
    def add(self, team):
        # Handled through events
        pass

    def find_by_ID(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        return self._team_from_row(row)
        
    def find_by_name(self, name):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}  WHERE Name=?', [name])
        row = cursor.fetchone()
        return self._team_from_row(row)
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}')
        return [self._team_from_row(row) for row in cursor.fetchall()]
        
    def dump(self):
        print('Teams:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
    
    def _team_from_row(self, row):
        if row is not None:
            return Team(self._event_bus, TeamID(UUID(row[0])), row[1])
        else:
            return None
        
    def try_handle_event(self, event):
        if isinstance(event, TeamRegisteredEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?, ?)', [str(event.ID.value), event.name])
            return True
        else:
            return False

import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Team, TeamID, TeamRepository
from fbsrankings.event import TeamRegisteredEvent


class TeamTable (object):
    def __init__(self):
        self.name = 'team'
        self.columns = 'UUID, Name'
        
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             Name TEXT NOT NULL UNIQUE);''')
             
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
            
        print('Teams:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()


class TeamQueryHandler (TeamRepository):
    def __init__(self, connection, event_bus):
        super().__init__(event_bus)
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.table = TeamTable()

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
            return Team(self._event_bus, TeamID(UUID(row[0])), row[1])
        else:
            return None
            
            
class TeamEventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        event_bus.register_handler(TeamRegisteredEvent, self._handle_team_registered)
        
        self.table = TeamTable()
        
    def handle(self, event):
        if isinstance(event, TeamRegisteredEvent):
            self._handle_team_registered(event)
            return True
        else:
            return False

    def _handle_team_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)', [str(event.ID.value), event.name])

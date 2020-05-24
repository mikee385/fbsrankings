import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonRepository, SeasonSection
from fbsrankings.event import SeasonRegisteredEvent


class SeasonSectionTable (object):
    def __init__(self):
        self.name = 'seasonsection'
        self.columns = 'Name'

    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
        (Name TEXT NOT NULL UNIQUE);''')
        
        cursor.execute(f'SELECT {self.columns} from {self.name}')
        existing = [row[0] for row in cursor.fetchall()]
        for value in SeasonSection:
            if value.name not in existing:
                cursor.execute(f'INSERT INTO {self.name} ({self.columns}) VALUES (?)', [value.name])
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
            
        print('Season Sections:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
            

class SeasonTable (object):
    def __init__(self):
        self.name = 'season'
        self.columns = 'UUID, Year'
             
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             Year INT  NOT NULL UNIQUE);''')
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')

        print('Seasons:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()


class SeasonQueryHandler (SeasonRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.table = SeasonTable()

    def find_by_ID(self, ID):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._season_from_row(row)
        
    def find_by_year(self, year):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE Year=?', [year])
        row = cursor.fetchone()
        cursor.close()
        return self._season_from_row(row)
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}')
        items = [self._season_from_row(row) for row in cursor.fetchall()]
        cursor.close()
        return items
    
    def _season_from_row(self, row):
        if row is not None:
            return Season(self._event_bus, SeasonID(UUID(row[0])), row[1])
        else:
            return None
            

class SeasonEventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        event_bus.register_handler(SeasonRegisteredEvent, self._handle_season_registered)
        
        self.table = SeasonTable()
        
    def handle(self, event):
        if isinstance(event, SeasonRegisteredEvent):
            self._handle_season_registered(event)
            return True
        else:
            return False

    def _handle_season_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)', [str(event.ID.value), event.year])

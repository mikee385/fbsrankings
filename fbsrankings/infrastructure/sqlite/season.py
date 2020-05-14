import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonRepository as BaseRepository, SeasonSection
from fbsrankings.event import SeasonRegisteredEvent


class SeasonSectionTable (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self._table = 'seasonsection'
        self._columns = 'Name'
        
        with self._connection:
            self._connection.execute('BEGIN')
            cursor = self._connection.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (Name TEXT NOT NULL UNIQUE);''')
            cursor.execute(f'SELECT {self._columns} from {self._table}')
            existing = [row[0] for row in cursor.fetchall()]
            for value in SeasonSection:
                if value.name not in existing:
                    cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?)', [value.name])
                    
    def dump(self):
        print('Season Sections:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')


class SeasonRepository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.season_section = SeasonSectionTable(connection)
        
        self._table = 'season'
        self._columns = 'UUID, Year'
        
        cursor = self._connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (UUID TEXT NOT NULL UNIQUE,
             Year INT  NOT NULL UNIQUE);''')

    def find_by_ID(self, ID):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        return self._season_from_row(row)
        
    def find_by_year(self, year):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table} WHERE Year=?', [year])
        row = cursor.fetchone()
        return self._season_from_row(row)
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}')
        return [self._season_from_row(row) for row in cursor.fetchall()]
        
    def dump(self):
        print('Seasons:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
    
    def _season_from_row(self, row):
        if row is not None:
            return Season(self._event_bus, SeasonID(UUID(row[0])), row[1])
        else:
            return None
        
    def try_handle_event(self, event):
        if isinstance(event, SeasonRegisteredEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?, ?)', [str(event.ID.value), event.year])
            return True
        else:
            return False

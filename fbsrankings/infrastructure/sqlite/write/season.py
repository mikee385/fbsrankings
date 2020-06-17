import sqlite3
from uuid import UUID

from fbsrankings.domain import Season, SeasonID, SeasonRepository as BaseRepository
from fbsrankings.event import SeasonRegisteredEvent
from fbsrankings.infrastructure.sqlite.storage import SeasonTable


class SeasonRepository (BaseRepository):
    def __init__(self, connection, cursor, bus):
        super().__init__(bus)
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        self.table = SeasonTable()
        
        bus.register_handler(SeasonRegisteredEvent, self._handle_season_registered)

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
            return Season(self._bus, SeasonID(UUID(row[0])), row[1])
        else:
            return None

    def _handle_season_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?)', [str(event.ID.value), event.year])

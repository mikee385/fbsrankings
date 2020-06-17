import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.infrastructure.sqlite.write import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Transaction (object):
    def __init__(self, database, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        
        self._connection = sqlite3.connect(database)
        self._connection.isolation_level = None
        self._connection.execute('PRAGMA foreign_keys = ON')
        
        self._cursor = self._connection.cursor()
        self._cursor.execute("begin")
        
        self.season = SeasonRepository(self._connection, self._cursor, self._bus)
        self.team = TeamRepository(self._connection, self._cursor, self._bus)
        self.affiliation = AffiliationRepository(self._connection, self._cursor, self._bus)
        self.game = GameRepository(self._connection, self._cursor, self._bus)
        
    def commit(self):
        self._cursor.execute("commit")
        self._cursor.close()
        self._connection.close()
        
    def rollback(self):
        self._cursor.execute("rollback")
        self._cursor.close()
        self._connection.close()
        
    def close(self):
        try:
            self._cursor.close()
            self._connection.close()
        except sqlite3.ProgrammingError:
            pass
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

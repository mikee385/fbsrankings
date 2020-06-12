import sqlite3

from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.infrastructure import QueryFactory, UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.sqlite import SeasonSectionTable, SeasonTable, TeamTable, SubdivisionTable, AffiliationTable, GameStatusTable, GameTable
from fbsrankings.infrastructure.sqlite import SeasonQueryHandler, TeamQueryHandler, AffiliationQueryHandler, GameQueryHandler
from fbsrankings.infrastructure.sqlite import SeasonEventHandler, TeamEventHandler, AffiliationEventHandler, GameEventHandler
        
 
class DataSource (QueryFactory, UnitOfWorkFactory):
    def __init__(self, database):
        self._database = database
        
        connection = sqlite3.connect(database)
        try:
            connection.isolation_level = None
            connection.execute('PRAGMA foreign_keys = ON')
        
            cursor = connection.cursor()
            cursor.execute("begin")
            try:
                SeasonSectionTable().create(cursor)
                SubdivisionTable().create(cursor)
                GameStatusTable().create(cursor)
        
                SeasonTable().create(cursor)
                TeamTable().create(cursor)
                AffiliationTable().create(cursor)
                GameTable().create(cursor)
        
                cursor.execute("commit")
            except:
                cursor.execute("rollback")
                raise
            finally:
                cursor.close()
        finally:
            connection.close()
        
    def queries(self):
        return QueryProvider(self._database)
        
    def unit_of_work(self, bus):
        return UnitOfWork(self._database, bus)
        

class QueryProvider (object):
    def __init__(self, database):
        self._connection = sqlite3.connect(database)
        self._connection.execute('PRAGMA query_only = ON')
        
        bus = ReadOnlyEventBus()
        
        self.season = SeasonQueryHandler(self._connection, bus)
        self.team = TeamQueryHandler(self._connection, bus)
        self.affiliation = AffiliationQueryHandler(self._connection, bus)
        self.game = GameQueryHandler(self._connection, bus)
        
    def close(self):
        self._connection.close()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, database, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._outer_bus = bus
        self._inner_bus = EventRecorder(EventBus())
        
        self._connection = sqlite3.connect(database)
        self._connection.isolation_level = None
        self._connection.execute('PRAGMA foreign_keys = ON')
        
        self._cursor = self._connection.cursor()
        self._cursor.execute("begin")
        
        self._season_handler = SeasonEventHandler(self._cursor, self._inner_bus)
        self._team_handler = TeamEventHandler(self._cursor, self._inner_bus)
        self._affiliation_handler = AffiliationEventHandler(self._cursor, self._inner_bus)
        self._game_handler = GameEventHandler(self._cursor, self._inner_bus)
        
        self.season = SeasonQueryHandler(self._connection, self._inner_bus)
        self.team = TeamQueryHandler(self._connection, self._inner_bus)
        self.affiliation = AffiliationQueryHandler(self._connection, self._inner_bus)
        self.game = GameQueryHandler(self._connection, self._inner_bus)

    def commit(self):
        self._cursor.execute("commit")
        self._cursor.close()
        self._connection.close()
        
        for event in self._inner_bus.events:
            self._outer_bus.publish(event)
        self._inner_bus.clear()
        
    def rollback(self):
        self._cursor.execute("rollback")
        self._cursor.close()
        self._connection.close()
        
        self._inner_bus.clear()
        
    def close(self):
        try:
            self._cursor.close()
            self._connection.close()
        except sqlite3.ProgrammingError:
            pass
        
        self._inner_bus.clear()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

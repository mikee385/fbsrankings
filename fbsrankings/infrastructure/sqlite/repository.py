import sqlite3

from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.domain import Factory, Repository
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.sqlite import SeasonSectionTable, SeasonTable, SeasonQueryHandler, SeasonEventHandler, TeamTable, TeamQueryHandler, TeamEventHandler, SubdivisionTable, AffiliationTable, AffiliationQueryHandler, AffiliationEventHandler, GameStatusTable, GameTable, GameQueryHandler, GameEventHandler
        
 
class DataStore (UnitOfWorkFactory):
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
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self._database, event_bus)
        

class QueryHandler (Repository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        
        super().__init__(
            SeasonQueryHandler(connection, event_bus),
            TeamQueryHandler(connection, event_bus),
            AffiliationQueryHandler(connection, event_bus),
            GameQueryHandler(connection, event_bus)
        )
        

class EventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('connection must be of type sqlite3.Cursor')
        
        self.season = SeasonEventHandler(cursor, event_bus),
        self.team = TeamEventHandler(cursor, event_bus),
        self.affiliation = AffiliationEventHandler(cursor, event_bus),
        self.game = GameEventHandler(cursor, event_bus)
        

class QueryProvider (QueryHandler):
    def __init__(self, database):
        self._connection = sqlite3.connect(database)
        self._connection.execute('PRAGMA query_only = ON')
        
        super().__init__(self._connection, ReadOnlyEventBus())
        
    def close(self):
        self._connection.close()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, database, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._outer_event_bus = event_bus
        self._inner_event_bus = EventRecorder(EventBus())
        
        self._isclosed = False
        self._connection = sqlite3.connect(database)
        self._connection.isolation_level = None
        self._connection.execute('PRAGMA foreign_keys = ON')
        
        self._cursor = self._connection.cursor()
        self._cursor.execute("begin")
        
        self.factory = Factory(self._inner_event_bus)
        self.repository = QueryHandler(self._connection, self._inner_event_bus)
        self.event_handler = EventHandler(self._cursor, self._inner_event_bus)

    def commit(self):
        self._cursor.execute("commit")
        self._cursor.close()
        self._connection.close()
        self._isclosed = True
        
        for event in self._inner_event_bus.events:
            self._outer_event_bus.raise_event(event)
        self._inner_event_bus.clear()
        
    def rollback(self):
        self._cursor.execute("rollback")
        self._cursor.close()
        self._connection.close()
        self._isclosed = True
        
        self._inner_event_bus.clear()
        
    def close(self):
        if self._isclosed == False:
            self._cursor.close()
            self._connection.close()
        
        self._inner_event_bus.clear()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

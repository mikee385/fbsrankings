import sqlite3

from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.domain import Factory
from fbsrankings.infrastructure import QueryFactory, UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.sqlite import SeasonSectionTable, SeasonTable, TeamTable, SubdivisionTable, AffiliationTable, GameStatusTable, GameTable, QueryHandler, EventHandler
        
 
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
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self._database, event_bus)
        

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

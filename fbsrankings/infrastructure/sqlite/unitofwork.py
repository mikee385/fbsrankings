import sqlite3

from fbsrankings.common import EventRecorder
from fbsrankings.domain import Factory
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory as BaseUnitOfWorkFactory
from fbsrankings.infrastructure.sqlite import Repository


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, connection, event_bus):
        super().__init__(EventRecorder(event_bus))
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.factory = Factory(self.event_bus)
    
        self.repository = Repository(self._connection, self.event_bus)

    def commit(self):
        with self._connection:
            self._connection.execute('BEGIN')
            
            for event in self.event_bus.events:
                handled = False
            
                handled = self.repository.season.try_handle_event(event) or handled
                handled = self.repository.team.try_handle_event(event) or handled
                handled = self.repository.affiliation.try_handle_event(event) or handled
                handled = self.repository.game.try_handle_event(event) or handled
            
                if not handled:
                    raise ValueError(f'Unknown event type: {type(event)}')
        
 
class UnitOfWorkFactory (BaseUnitOfWorkFactory):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
    def create(self, event_bus):
        return UnitOfWork(self._connection, event_bus)

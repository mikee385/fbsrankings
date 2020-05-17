import sqlite3

from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.domain import Factory, Repository as BaseRepository
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.sqlite import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository
        
 
class DataStore (UnitOfWorkFactory):
    def __init__(self, db_filename):
        self._connection = sqlite3.connect(db_filename)
        self._connection.execute('PRAGMA foreign_keys = ON')
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self._connection, event_bus)


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, connection, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._outer_event_bus = event_bus
        self._inner_event_bus = EventRecorder(EventBus())
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.factory = Factory(self._inner_event_bus)
        self.repository = Repository(self._connection, self._inner_event_bus)

    def commit(self):
        with self._connection:
            self._connection.execute('BEGIN')
            
            for event in self._inner_event_bus.events:
                handled = False
            
                handled = self.repository.season.try_handle_event(event) or handled
                handled = self.repository.team.try_handle_event(event) or handled
                handled = self.repository.affiliation.try_handle_event(event) or handled
                handled = self.repository.game.try_handle_event(event) or handled
            
                if not handled:
                    raise ValueError(f'Unknown event type: {type(event)}')

        for event in self._inner_event_bus.events:
            self._outer_event_bus.raise_event(event)
        self._inner_event_bus.clear()


class Repository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        
        super().__init__(
            SeasonRepository(connection, event_bus),
            TeamRepository(connection, event_bus),
            AffiliationRepository(connection, event_bus),
            GameRepository(connection, event_bus)
        )

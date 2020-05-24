from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.domain import Factory, Repository
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.memory import SeasonDataStore, TeamDataStore, AffiliationDataStore, GameDataStore
from fbsrankings.infrastructure.memory import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class DataStore (UnitOfWorkFactory):
    def __init__(self):
        self.event_bus = EventBus()

        self.season = SeasonDataStore()
        self.team = TeamDataStore()
        self.affiliation = AffiliationDataStore()
        self.game = GameDataStore()
        
    def queries (self):
        return QueryProvider(self)
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self, event_bus)
        

class QueryHandler (Repository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, DataStore):
            raise TypeError('data_store must be of type DataStore')
        
        super().__init__(
            SeasonRepository(data_store.season, event_bus),
            TeamRepository(data_store.team, event_bus),
            AffiliationRepository(data_store.affiliation, event_bus),
            GameRepository(data_store.game, event_bus)
        )
        

class QueryProvider (QueryHandler):
    def __init__(self, data_store):
        super().__init__(data_store, ReadOnlyEventBus())
        
    def close(self):
        pass
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        return False


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, data_store, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._outer_event_bus = event_bus
        self._inner_event_bus = EventRecorder(EventBus())
        
        if not isinstance(data_store, DataStore):
            raise TypeError('data_store must be of type DataStore')
        self.data_store = data_store
        
        self.factory = Factory(self._inner_event_bus)
        self.repository = QueryHandler(data_store, self._inner_event_bus)

    def commit(self):
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
        
    def rollback(self):
        self._inner_event_bus.clear()
        
    def close(self):
        self._inner_event_bus.clear()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

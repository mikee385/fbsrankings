from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.domain import Factory, Repository as BaseRepository
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.memory import SeasonDataStore, TeamDataStore, AffiliationDataStore, GameDataStore
from fbsrankings.infrastructure.memory import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class DataStore (UnitOfWorkFactory):
    def __init__(self):
        self.event_bus = EventBus()

        self.season = SeasonDataStore(self.event_bus)
        self.team = TeamDataStore(self.event_bus)
        self.affiliation = AffiliationDataStore(self.event_bus)
        self.game = GameDataStore(self.event_bus)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self, event_bus)


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
        self.repository = Repository(data_store, self._inner_event_bus)

    def commit(self):
        for event_type in self._inner_event_bus.types:
            self.data_store.event_bus.register_type(event_type)
            
        for event in self._inner_event_bus.events:
            handled = False
            
            handled = self.repository.season.try_handle_event(event) or handled
            handled = self.repository.team.try_handle_event(event) or handled
            handled = self.repository.affiliation.try_handle_event(event) or handled
            handled = self.repository.game.try_handle_event(event) or handled
            
            if not handled:
                raise ValueError(f'Unknown event type: {type(event)}')
                
        for event_type in self._inner_event_bus.types:
            self._outer_event_bus.register_type(event_type)        
        for event in self._inner_event_bus.events:
            self._outer_event_bus.raise_event(event)
        self._inner_event_bus.clear()


class Repository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, DataStore):
            raise TypeError('data_store must be of type DataStore')
        
        super().__init__(
            SeasonRepository(data_store.season, event_bus), 
            TeamRepository(data_store.team, event_bus), 
            AffiliationRepository(data_store.affiliation, event_bus), 
            GameRepository(data_store.game, event_bus)
        )

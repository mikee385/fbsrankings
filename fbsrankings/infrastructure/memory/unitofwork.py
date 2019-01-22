from fbsrankings.common import EventRecorder
from fbsrankings.domain import Factory
from fbsrankings.infrastructure import UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory as BaseUnitOfWorkFactory
from fbsrankings.infrastructure.memory import DataStore, Repository


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, data_store, event_bus):
        super().__init__(EventRecorder(event_bus))
        
        self.data_store = data_store
        
        self.factory = Factory(self.event_bus)
    
        self.repository = Repository(data_store, self.event_bus)

    def commit(self):
        for event_type in self.event_bus.types:
            self.data_store.event_bus.register_type(event_type)
            
        for event in self.event_bus.events:
            handled = False
            
            handled = self.repository.season.try_handle_event(event) or handled
            handled = self.repository.team.try_handle_event(event) or handled
            handled = self.repository.affiliation.try_handle_event(event) or handled
            handled = self.repository.game.try_handle_event(event) or handled
            
            if not handled:
                raise ValueError(f'Unknown event type: {type(event)}')
        
 
class UnitOfWorkFactory (BaseUnitOfWorkFactory):
    def __init__(self, data_store):
        if not isinstance(data_store, DataStore):
            raise TypeError('data_store must be of type DataStore')
        self._data_store = data_store
        
    def create(self, event_bus):
        return UnitOfWork(self._data_store, event_bus)

from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.infrastructure import QueryFactory, UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.memory import SeasonDataSource, TeamDataSource, AffiliationDataSource, GameDataSource, QueryHandler, EventHandler


class DataSource (QueryFactory, UnitOfWorkFactory):
    def __init__(self):
        self.event_bus = EventBus()

        self.season = SeasonDataSource()
        self.team = TeamDataSource()
        self.affiliation = AffiliationDataSource()
        self.game = GameDataSource()
        
    def queries(self):
        return QueryProvider(self)
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self, event_bus)
        

class QueryProvider (QueryHandler):
    def __init__(self, data_source):
        super().__init__(data_source, ReadOnlyEventBus())
        
    def close(self):
        pass
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        return False


class UnitOfWork (BaseUnitOfWork):
    def __init__(self, data_source, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._outer_event_bus = event_bus
        self._inner_event_bus = EventRecorder(EventBus())
        
        if not isinstance(data_source, DataSource):
            raise TypeError('data_source must be of type DataSource')
        self.data_source = data_source
        
        self._query_handler = QueryHandler(data_source, self._inner_event_bus)
        self._event_handler = EventHandler(data_source, self._inner_event_bus)
        
        self.season = self._query_handler.season
        self.team = self._query_handler.team
        self.affiliation = self._query_handler.affiliation
        self.game = self._query_handler.game

    def commit(self):
        for event in self._inner_event_bus.events:
            handled = self._event_handler.handle(event)
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

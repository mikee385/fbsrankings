from fbsrankings.common import EventBus, ReadOnlyEventBus, EventRecorder
from fbsrankings.infrastructure import QueryFactory, UnitOfWork as BaseUnitOfWork, UnitOfWorkFactory
from fbsrankings.infrastructure.memory import SeasonDataSource, TeamDataSource, AffiliationDataSource, GameDataSource
from fbsrankings.infrastructure.memory import SeasonQueryHandler, TeamQueryHandler, AffiliationQueryHandler, GameQueryHandler
from fbsrankings.infrastructure.memory import SeasonEventHandler, TeamEventHandler, AffiliationEventHandler, GameEventHandler


class DataSource (QueryFactory, UnitOfWorkFactory):
    def __init__(self):
        self.season = SeasonDataSource()
        self.team = TeamDataSource()
        self.affiliation = AffiliationDataSource()
        self.game = GameDataSource()
        
    def queries(self):
        return QueryProvider(self)
        
    def unit_of_work(self, event_bus):
        return UnitOfWork(self, event_bus)
        

class QueryProvider (object):
    def __init__(self, data_source):
        event_bus = ReadOnlyEventBus()
        
        self.season = SeasonQueryHandler(data_source.season, event_bus)
        self.team = TeamQueryHandler(data_source.team, event_bus)
        self.affiliation = AffiliationQueryHandler(data_source.affiliation, event_bus)
        self.game = GameQueryHandler(data_source.game, event_bus)
        
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
        
        self._season_handler = SeasonEventHandler(data_source.season, self._inner_event_bus)
        self._team_handler = TeamEventHandler(data_source.team, self._inner_event_bus)
        self._affiliation_handler = AffiliationEventHandler(data_source.affiliation, self._inner_event_bus)
        self._game_handler = GameEventHandler(data_source.game, self._inner_event_bus)
        
        self.season = SeasonQueryHandler(data_source.season, self._inner_event_bus)
        self.team = TeamQueryHandler(data_source.team, self._inner_event_bus)
        self.affiliation = AffiliationQueryHandler(data_source.affiliation, self._inner_event_bus)
        self.game = GameQueryHandler(data_source.game, self._inner_event_bus)

    def commit(self):
        for event in self._inner_event_bus.events:
            handled = False
        
            handled = self._season_handler.handle(event) or handled
            handled = self._team_handler.handle(event) or handled
            handled = self._affiliation_handler.handle(event) or handled
            handled = self._game_handler.handle(event) or handled
            
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
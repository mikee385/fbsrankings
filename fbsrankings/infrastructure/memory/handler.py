from fbsrankings.common import EventBus
from fbsrankings.infrastructure.memory import SeasonQueryHandler, SeasonEventHandler, TeamQueryHandler, TeamEventHandler, AffiliationQueryHandler, AffiliationEventHandler, GameQueryHandler, GameEventHandler


class QueryHandler (object):
    def __init__(self, data_source, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        
        self.season = SeasonQueryHandler(data_source.season, event_bus)
        self.team = TeamQueryHandler(data_source.team, event_bus)
        self.affiliation = AffiliationQueryHandler(data_source.affiliation, event_bus)
        self.game = GameQueryHandler(data_source.game, event_bus)
        

class EventHandler (object):
    def __init__(self, data_source, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        
        self.season = SeasonEventHandler(data_source.season, event_bus)
        self.team = TeamEventHandler(data_source.team, event_bus)
        self.affiliation = AffiliationEventHandler(data_source.affiliation, event_bus)
        self.game = GameEventHandler(data_source.game, event_bus)
        
    def handle(self, event):
        handled = False
        
        handled = self.season.handle(event) or handled
        handled = self.team.handle(event) or handled
        handled = self.affiliation.handle(event) or handled
        handled = self.game.handle(event) or handled
        
        return handled

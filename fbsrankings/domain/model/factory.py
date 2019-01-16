from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory


class Factory (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
            
        self.season = SeasonFactory(event_bus)
        self.team = TeamFactory(event_bus)
        self.affiliation = AffiliationFactory(event_bus)
        self.game = GameFactory(event_bus)

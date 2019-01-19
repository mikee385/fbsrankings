from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory
from fbsrankings.infrastructure.local import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class UnitOfWork (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self.event_bus = EventRecorder(event_bus)
        
        self.season_factory = SeasonFactory(self.event_bus)
        self.team_factory = TeamFactory(self.event_bus)
        self.affiliation_factory = AffiliationFactory(self.event_bus)
        self.game_factory = GameFactory(self.event_bus)
        
        self.season_repository = SeasonRepository(self.event_bus)
        self.team_repository = TeamRepository(self.event_bus)
        self.affiliation_repository = AffiliationRepository(self.event_bus)
        self.game_repository = GameRepository(self.event_bus)

    def commit(self):
        pass

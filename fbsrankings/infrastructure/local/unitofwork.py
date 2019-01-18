from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory
from fbsrankings.infrastructure.local import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class UnitOfWork (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.season_factory = SeasonFactory(self._event_bus)
        self.team_factory = TeamFactory(self._event_bus)
        self.affiliation_factory = AffiliationFactory(self._event_bus)
        self.game_factory = GameFactory(self._event_bus)
        
        self.season_repository = SeasonRepository(self._event_bus)
        self.team_repository = TeamRepository(self._event_bus)
        self.affiliation_repository = AffiliationRepository(self._event_bus)
        self.game_repository = GameRepository(self._event_bus)

    def commit(self):
        pass

from fbsrankings.domain.season import SeasonFactory
from fbsrankings.domain.team import TeamFactory
from fbsrankings.domain.affiliation import AffiliationFactory
from fbsrankings.domain.game import GameFactory


class Factory (SeasonFactory, TeamFactory, AffiliationFactory, GameFactory):
    def __init__(self, event_bus):
        SeasonFactory.__init__(self, event_bus)
        TeamFactory.__init__(self, event_bus)
        AffiliationFactory.__init__(self, event_bus)
        GameFactory.__init__(self, event_bus)

from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory


class Factory (SeasonFactory, TeamFactory, AffiliationFactory, GameFactory):
    def __init__(self, event_bus):
        SeasonFactory.__init__(self, event_bus)
        TeamFactory.__init__(self, event_bus)
        AffiliationFactory.__init__(self, event_bus)
        GameFactory.__init__(self, event_bus)

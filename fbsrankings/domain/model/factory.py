from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory


class Factory (object):
    def __init__(self, event_bus):
        self.season = SeasonFactory(event_bus)
        self.team = TeamFactory(event_bus)
        self.affiliation = AffiliationFactory(event_bus)
        self.game = GameFactory(event_bus)

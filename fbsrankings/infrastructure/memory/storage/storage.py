from fbsrankings.infrastructure.memory.storage import SeasonStorage, TeamStorage, AffiliationStorage, GameStorage


class Storage (object):
    def __init__(self) -> None:
        self.season = SeasonStorage()
        self.team = TeamStorage()
        self.affiliation = AffiliationStorage()
        self.game = GameStorage()

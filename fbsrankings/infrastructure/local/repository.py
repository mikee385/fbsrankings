from fbsrankings.infrastructure.local import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Repository (object):
    def __init__(self):
        self.season = SeasonRepository()
        self.team = TeamRepository()
        self.affiliation = AffiliationRepository()
        self.game = GameRepository()

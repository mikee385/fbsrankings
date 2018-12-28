from fbsrankings.infrastructure.local import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Repository(SeasonRepository, TeamRepository, GameRepository, AffiliationRepository):
    def __init__(self):
        SeasonRepository.__init__(self)
        TeamRepository.__init__(self)
        AffiliationRepository.__init__(self)
        GameRepository.__init__(self)

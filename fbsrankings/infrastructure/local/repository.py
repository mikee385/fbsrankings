from fbsrankings.infrastructure.local.seasonrepository import SeasonRepository
from fbsrankings.infrastructure.local.teamrepository import TeamRepository
from fbsrankings.infrastructure.local.affiliationrepository import AffiliationRepository
from fbsrankings.infrastructure.local.gamerepository import GameRepository


class Repository(SeasonRepository, TeamRepository, GameRepository, AffiliationRepository):
    def __init__(self):
        SeasonRepository.__init__(self)
        TeamRepository.__init__(self)
        AffiliationRepository.__init__(self)
        GameRepository.__init__(self)
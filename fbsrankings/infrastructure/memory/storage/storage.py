from fbsrankings.infrastructure.memory.storage.affiliation import AffiliationStorage
from fbsrankings.infrastructure.memory.storage.game import GameStorage
from fbsrankings.infrastructure.memory.storage.ranking import RankingStorage
from fbsrankings.infrastructure.memory.storage.season import SeasonStorage
from fbsrankings.infrastructure.memory.storage.team import TeamStorage


class Storage(object):
    def __init__(self) -> None:
        self.season = SeasonStorage()
        self.team = TeamStorage()
        self.affiliation = AffiliationStorage()
        self.game = GameStorage()
        self.team_ranking = RankingStorage()
        self.game_ranking = RankingStorage()

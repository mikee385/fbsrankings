from fbsrankings.infrastructure.memory.storage.affiliation import AffiliationStorage
from fbsrankings.infrastructure.memory.storage.game import GameStorage
from fbsrankings.infrastructure.memory.storage.ranking import RankingStorage
from fbsrankings.infrastructure.memory.storage.record import TeamRecordStorage
from fbsrankings.infrastructure.memory.storage.season import SeasonStorage
from fbsrankings.infrastructure.memory.storage.team import TeamStorage


class Storage:
    def __init__(self) -> None:
        self.season = SeasonStorage()
        self.team = TeamStorage()
        self.affiliation = AffiliationStorage()
        self.game = GameStorage()

        self.team_record = TeamRecordStorage()
        self.team_ranking = RankingStorage()
        self.game_ranking = RankingStorage()

    def drop(self) -> None:
        self.season.drop()
        self.team.drop()
        self.affiliation.drop()
        self.game.drop()

        self.team_record.drop()
        self.team_ranking.drop()
        self.game_ranking.drop()

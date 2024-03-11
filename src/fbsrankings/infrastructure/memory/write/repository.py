from fbsrankings.common import EventBus
from fbsrankings.infrastructure import Repository as BaseRepository
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write.affiliation import AffiliationRepository
from fbsrankings.infrastructure.memory.write.game import GameRepository
from fbsrankings.infrastructure.memory.write.ranking import GameRankingRepository
from fbsrankings.infrastructure.memory.write.ranking import TeamRankingRepository
from fbsrankings.infrastructure.memory.write.record import TeamRecordRepository
from fbsrankings.infrastructure.memory.write.season import SeasonRepository
from fbsrankings.infrastructure.memory.write.team import TeamRepository


class Repository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = bus

        self._season = SeasonRepository(storage.season, self._bus)
        self._team = TeamRepository(storage.team, self._bus)
        self._affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self._game = GameRepository(storage.game, self._bus)

        self._team_record = TeamRecordRepository(storage.team_record, self._bus)
        self._team_ranking = TeamRankingRepository(storage.team_ranking, self._bus)
        self._game_ranking = GameRankingRepository(storage.game_ranking, self._bus)

    @property
    def season(self) -> SeasonRepository:
        return self._season

    @property
    def team(self) -> TeamRepository:
        return self._team

    @property
    def affiliation(self) -> AffiliationRepository:
        return self._affiliation

    @property
    def game(self) -> GameRepository:
        return self._game

    @property
    def team_record(self) -> TeamRecordRepository:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

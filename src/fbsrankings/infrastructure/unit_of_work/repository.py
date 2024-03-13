from fbsrankings.common import EventBus
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import GameRankingRepository
from fbsrankings.domain import GameRepository
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import TeamRankingRepository
from fbsrankings.domain import TeamRecordRepository
from fbsrankings.domain import TeamRepository
from fbsrankings.infrastructure.memory.write import Repository as MemoryRepository
from fbsrankings.infrastructure.repository import Repository as BaseRepository
from fbsrankings.infrastructure.unit_of_work.affiliation import (
    AffiliationRepository as UnitOfWorkAffilationRepository,
)
from fbsrankings.infrastructure.unit_of_work.game import (
    GameRepository as UnitOfWorkGameRepository,
)
from fbsrankings.infrastructure.unit_of_work.ranking import (
    GameRankingRepository as UnitOfWorkGameRankingRepository,
)
from fbsrankings.infrastructure.unit_of_work.ranking import (
    TeamRankingRepository as UnitOfWorkTeamRankingRepository,
)
from fbsrankings.infrastructure.unit_of_work.record import (
    TeamRecordRepository as UnitOfWorkTeamRecordRepository,
)
from fbsrankings.infrastructure.unit_of_work.season import (
    SeasonRepository as UnitOfWorkSeasonRepository,
)
from fbsrankings.infrastructure.unit_of_work.team import (
    TeamRepository as UnitOfWorkTeamRepository,
)


class Repository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        storage_bus: EventBus,
    ) -> None:
        self._season = UnitOfWorkSeasonRepository(
            repository.season,
            cache.season,
            storage_bus,
        )
        self._team = UnitOfWorkTeamRepository(repository.team, cache.team, storage_bus)
        self._affiliation = UnitOfWorkAffilationRepository(
            repository.affiliation,
            cache.affiliation,
            storage_bus,
        )
        self._game = UnitOfWorkGameRepository(repository.game, cache.game, storage_bus)
        self._team_record = UnitOfWorkTeamRecordRepository(
            repository.team_record,
            cache.team_record,
            storage_bus,
        )
        self._team_ranking = UnitOfWorkTeamRankingRepository(
            repository.team_ranking,
            cache.team_ranking,
            storage_bus,
        )
        self._game_ranking = UnitOfWorkGameRankingRepository(
            repository.game_ranking,
            cache.game_ranking,
            storage_bus,
        )

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

from fbsrankings.common import EventBus
from fbsrankings.ranking.command.domain.model.ranking import GameRankingRepository
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingRepository
from fbsrankings.ranking.command.domain.model.record import TeamRecordRepository
from fbsrankings.ranking.command.infrastructure.memory.repository import (
    Repository as MemoryRepository,
)
from fbsrankings.ranking.command.infrastructure.repository import (
    Repository as BaseRepository,
)
from fbsrankings.ranking.command.infrastructure.unit_of_work.ranking import (
    GameRankingRepository as UnitOfWorkGameRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.unit_of_work.ranking import (
    TeamRankingRepository as UnitOfWorkTeamRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.unit_of_work.record import (
    TeamRecordRepository as UnitOfWorkTeamRecordRepository,
)


class Repository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        storage_bus: EventBus,
    ) -> None:
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
    def team_record(self) -> TeamRecordRepository:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

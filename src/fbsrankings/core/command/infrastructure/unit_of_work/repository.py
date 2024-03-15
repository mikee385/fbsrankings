from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.affiliation import AffiliationRepository
from fbsrankings.core.command.domain.model.game import GameRepository
from fbsrankings.core.command.domain.model.season import SeasonRepository
from fbsrankings.core.command.domain.model.team import TeamRepository
from fbsrankings.core.command.infrastructure.memory.repository import (
    Repository as MemoryRepository,
)
from fbsrankings.core.command.infrastructure.repository import (
    Repository as BaseRepository,
)
from fbsrankings.core.command.infrastructure.unit_of_work.affiliation import (
    AffiliationRepository as UnitOfWorkAffilationRepository,
)
from fbsrankings.core.command.infrastructure.unit_of_work.game import (
    GameRepository as UnitOfWorkGameRepository,
)
from fbsrankings.core.command.infrastructure.unit_of_work.season import (
    SeasonRepository as UnitOfWorkSeasonRepository,
)
from fbsrankings.core.command.infrastructure.unit_of_work.team import (
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

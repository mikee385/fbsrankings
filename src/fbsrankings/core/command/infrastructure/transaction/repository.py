from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import AffiliationRepository
from fbsrankings.core.command.domain.model.game import GameRepository
from fbsrankings.core.command.domain.model.repository import (
    Repository as BaseRepository,
)
from fbsrankings.core.command.domain.model.season import SeasonRepository
from fbsrankings.core.command.domain.model.team import TeamRepository
from fbsrankings.core.command.infrastructure.memory.repository import (
    Repository as MemoryRepository,
)
from fbsrankings.core.command.infrastructure.transaction.affiliation import (
    AffiliationRepository as TransactionAffilationRepository,
)
from fbsrankings.core.command.infrastructure.transaction.game import (
    GameRepository as TransactionGameRepository,
)
from fbsrankings.core.command.infrastructure.transaction.season import (
    SeasonRepository as TransactionSeasonRepository,
)
from fbsrankings.core.command.infrastructure.transaction.team import (
    TeamRepository as TransactionTeamRepository,
)


class Repository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        storage_bus: EventBus,
    ) -> None:
        self._season = TransactionSeasonRepository(
            repository.season,
            cache.season,
            storage_bus,
        )
        self._team = TransactionTeamRepository(repository.team, cache.team, storage_bus)
        self._affiliation = TransactionAffilationRepository(
            repository.affiliation,
            cache.affiliation,
            storage_bus,
        )
        self._game = TransactionGameRepository(repository.game, cache.game, storage_bus)

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

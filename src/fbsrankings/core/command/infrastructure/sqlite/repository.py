from fbsrankings.common import EventBus
from fbsrankings.core.command.infrastructure.repository import (
    Repository as BaseRepository,
)
from fbsrankings.core.command.infrastructure.sqlite.affiliation import (
    AffiliationRepository,
)
from fbsrankings.core.command.infrastructure.sqlite.game import GameRepository
from fbsrankings.core.command.infrastructure.sqlite.season import SeasonRepository
from fbsrankings.core.command.infrastructure.sqlite.team import TeamRepository
from fbsrankings.storage.sqlite import Storage


class Repository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._season = SeasonRepository(storage, bus)
        self._team = TeamRepository(storage, bus)
        self._affiliation = AffiliationRepository(storage, bus)
        self._game = GameRepository(storage, bus)

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

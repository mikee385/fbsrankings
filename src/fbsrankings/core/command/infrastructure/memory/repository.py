from fbsrankings.common import EventBus
from fbsrankings.core.command.infrastructure.memory.affiliation import (
    AffiliationRepository,
)
from fbsrankings.core.command.infrastructure.memory.game import GameRepository
from fbsrankings.core.command.infrastructure.memory.season import SeasonRepository
from fbsrankings.core.command.infrastructure.memory.team import TeamRepository
from fbsrankings.core.command.infrastructure.repository import (
    Repository as BaseRepository,
)
from fbsrankings.storage.memory import Storage


class Repository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = bus

        self._season = SeasonRepository(storage.season, self._bus)
        self._team = TeamRepository(storage.team, self._bus)
        self._affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self._game = GameRepository(storage.game, self._bus)

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

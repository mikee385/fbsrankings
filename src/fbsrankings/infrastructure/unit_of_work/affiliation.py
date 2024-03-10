from typing import Optional

from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import SeasonID
from fbsrankings.domain import Subdivision
from fbsrankings.domain import TeamID
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.infrastructure.memory.storage import (
    AffiliationStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    AffiliationRepository as MemoryRepository,
)


class AffiliationRepository(BaseRepository):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(AffiliationCreatedEvent, self._cache.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(
            AffiliationCreatedEvent,
            self._cache.handle_created,
        )

    def create(
        self,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        return self._repository.create(season_id, team_id, subdivision)

    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        affiliation = self._cache.get(id_)
        if affiliation is None:
            affiliation = self._repository.get(id_)
        return affiliation

    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        affiliation = self._cache.find(season_id, team_id)
        if affiliation is None:
            affiliation = self._repository.find(season_id, team_id)
        return affiliation

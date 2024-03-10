from typing import Optional

from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.memory.storage import (
    SeasonStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    SeasonRepository as MemoryRepository,
)


class SeasonRepository(BaseRepository):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(SeasonCreatedEvent, self._cache.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(SeasonCreatedEvent, self._cache.handle_created)

    def create(self, year: int) -> Season:
        return self._repository.create(year)

    def get(self, id_: SeasonID) -> Optional[Season]:
        season = self._cache.get(id_)
        if season is None:
            season = self._repository.get(id_)
        return season

    def find(self, year: int) -> Optional[Season]:
        season = self._cache.find(year)
        if season is None:
            season = self._repository.find(year)
        return season

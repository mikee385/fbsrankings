from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonEventHandler as BaseEventHandler
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.memory.write import (
    SeasonRepository as MemoryRepository,
)


class SeasonRepository(BaseRepository):
    def __init__(self, repository: BaseRepository, cache: MemoryRepository) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

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


class SeasonEventHandler(BaseEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_created(self, event: SeasonCreatedEvent) -> None:
        self._events.append(event)

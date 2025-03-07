from typing import List
from typing import Optional
from uuid import uuid4

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.season import (
    SeasonRepository as BaseRepository,
)
from fbsrankings.core.command.infrastructure.memory.season import (
    SeasonRepository as MemoryRepository,
)
from fbsrankings.messages.event import SeasonCreatedEvent
from fbsrankings.messages.event import SeasonEventHandler as BaseEventHandler


class SeasonRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

    def get(self, id_: SeasonID) -> Optional[Season]:
        season = self._cache.get(id_)
        if season is None:
            season = self._repository.get(id_)
            if season is not None:
                self._cache_bus.publish(_created_event(season))
        return season

    def find(self, year: int) -> Optional[Season]:
        season = self._cache.find(year)
        if season is None:
            season = self._repository.find(year)
            if season is not None:
                self._cache_bus.publish(_created_event(season))
        return season


def _created_event(season: Season) -> SeasonCreatedEvent:
    return SeasonCreatedEvent(str(uuid4()), str(season.id_), season.year)


class SeasonEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: SeasonCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

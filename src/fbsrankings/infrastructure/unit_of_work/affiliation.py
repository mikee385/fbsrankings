from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationEventHandler as BaseEventHandler
from fbsrankings.domain import AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import SeasonID
from fbsrankings.domain import Subdivision
from fbsrankings.domain import TeamID
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.infrastructure.memory.write import (
    AffiliationRepository as MemoryRepository,
)


class AffiliationRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(repository._bus)
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
            if affiliation is not None:
                self._cache_bus.publish(_created_event(affiliation))
        return affiliation

    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        affiliation = self._cache.find(season_id, team_id)
        if affiliation is None:
            affiliation = self._repository.find(season_id, team_id)
            if affiliation is not None:
                self._cache_bus.publish(_created_event(affiliation))
        return affiliation


def _created_event(affiliation: Affiliation) -> AffiliationCreatedEvent:
    return AffiliationCreatedEvent(
        affiliation.id_.value,
        affiliation.season_id.value,
        affiliation.team_id.value,
        affiliation.subdivision.name,
    )


class AffiliationEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(event_bus)
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

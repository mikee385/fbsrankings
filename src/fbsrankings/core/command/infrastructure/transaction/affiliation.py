from typing import List
from typing import Optional
from uuid import uuid4

from communication.bus import Event
from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.affiliation import AffiliationID
from fbsrankings.core.command.domain.model.affiliation import (
    AffiliationRepository as BaseRepository,
)
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.infrastructure.memory.affiliation import (
    AffiliationRepository as MemoryRepository,
)
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.event import AffiliationEventHandler as BaseEventHandler


class AffiliationRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
        uuid4(),
        affiliation.id_,
        affiliation.season_id,
        affiliation.team_id,
        affiliation.subdivision.name,
    )


class AffiliationEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

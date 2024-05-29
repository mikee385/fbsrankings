from typing import List
from typing import Optional

from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.core.command.infrastructure.memory.team import (
    TeamRepository as MemoryRepository,
)
from fbsrankings.shared.event import TeamCreatedEvent
from fbsrankings.shared.event import TeamEventHandler as BaseEventHandler
from fbsrankings.shared.messaging import Event
from fbsrankings.shared.messaging import EventBus


class TeamRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

    def get(self, id_: TeamID) -> Optional[Team]:
        team = self._cache.get(id_)
        if team is None:
            team = self._repository.get(id_)
            if team is not None:
                self._cache_bus.publish(_created_event(team))
        return team

    def find(self, name: str) -> Optional[Team]:
        team = self._cache.find(name)
        if team is None:
            team = self._repository.find(name)
            if team is not None:
                self._cache_bus.publish(_created_event(team))
        return team


def _created_event(team: Team) -> TeamCreatedEvent:
    return TeamCreatedEvent(team.id_, team.name)


class TeamEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

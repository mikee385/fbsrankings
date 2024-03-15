from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import (
    TeamEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.core.command.event.team import TeamCreatedEvent
from fbsrankings.core.command.infrastructure.memory.team import (
    TeamRepository as MemoryRepository,
)


class TeamRepository(BaseRepository):
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

    def create(self, name: str) -> Team:
        return self._repository.create(name)

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
    return TeamCreatedEvent(team.id_.value, team.name)


class TeamEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(event_bus)
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

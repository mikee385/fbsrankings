from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Team
from fbsrankings.domain import TeamEventHandler as BaseEventHandler
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.memory.write import (
    TeamRepository as MemoryRepository,
)


class TeamRepository(BaseRepository):
    def __init__(self, repository: BaseRepository, cache: MemoryRepository) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

    def create(self, name: str) -> Team:
        return self._repository.create(name)

    def get(self, id_: TeamID) -> Optional[Team]:
        team = self._cache.get(id_)
        if team is None:
            team = self._repository.get(id_)
        return team

    def find(self, name: str) -> Optional[Team]:
        team = self._cache.find(name)
        if team is None:
            team = self._repository.find(name)
        return team


class TeamEventHandler(BaseEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._events.append(event)

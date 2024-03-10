from typing import Optional

from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.memory.storage import (
    TeamStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    TeamRepository as MemoryRepository,
)


class TeamRepository(BaseRepository):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(TeamCreatedEvent, self._cache.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(TeamCreatedEvent, self._cache.handle_created)

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

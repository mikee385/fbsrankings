from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.memory.storage import TeamDto
from fbsrankings.infrastructure.memory.storage import TeamStorage


class TeamRepository(BaseRepository):
    def __init__(self, storage: TeamStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, id: TeamID) -> Optional[Team]:
        dto = self._storage.get(id.value)
        return self._to_team(dto) if dto is not None else None

    def find(self, name: str) -> Optional[Team]:
        dto = self._storage.find(name)
        return self._to_team(dto) if dto is not None else None

    def all(self) -> List[Team]:
        dtos = self._storage.all()
        return [self._to_team(dto) for dto in dtos if dto is not None]

    def _to_team(self, dto: TeamDto) -> Team:
        return Team(self._bus, TeamID(dto.id), dto.name)

    def handle(self, event: Event) -> bool:
        if isinstance(event, TeamCreatedEvent):
            self._handle_team_created(event)
            return True
        return False

    def _handle_team_created(self, event: TeamCreatedEvent) -> None:
        self._storage.add(TeamDto(event.id, event.name))

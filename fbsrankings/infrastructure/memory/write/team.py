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

    def get(self, ID: TeamID) -> Optional[Team]:
        return self._to_team(self._storage.get(ID.value))

    def find(self, name: str) -> Optional[Team]:
        return self._to_team(self._storage.find(name))

    def _to_team(self, dto: Optional[TeamDto]) -> Optional[Team]:
        if dto is not None:
            return Team(self._bus, TeamID(dto.ID), dto.name)
        return None

    def handle(self, event: Event) -> bool:
        if isinstance(event, TeamCreatedEvent):
            self._handle_team_created(event)
            return True
        else:
            return False

    def _handle_team_created(self, event: TeamCreatedEvent) -> None:
        self._storage.add(TeamDto(event.ID, event.name))

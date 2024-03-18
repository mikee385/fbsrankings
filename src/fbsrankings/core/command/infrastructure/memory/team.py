from typing import Optional

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import (
    TeamEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.domain.model.team import TeamRepository as BaseRepository
from fbsrankings.core.command.event.team import TeamCreatedEvent
from fbsrankings.storage.memory import TeamDto
from fbsrankings.storage.memory import TeamStorage


class TeamRepository(BaseRepository):
    def __init__(self, storage: TeamStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, id_: TeamID) -> Optional[Team]:
        dto = self._storage.get(id_)
        return self._to_team(dto) if dto is not None else None

    def find(self, name: str) -> Optional[Team]:
        dto = self._storage.find(name)
        return self._to_team(dto) if dto is not None else None

    def _to_team(self, dto: TeamDto) -> Team:
        return Team(self._bus, TeamID(dto.id_), dto.name)


class TeamEventHandler(BaseEventHandler):
    def __init__(self, storage: TeamStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def handle_created(self, event: TeamCreatedEvent) -> None:
        self._storage.add(TeamDto(event.id_, event.name))

from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.memory.storage import TeamDto
from fbsrankings.infrastructure.memory.storage import TeamStorage


class TeamRepository(BaseRepository, ContextManager["TeamRepository"]):
    def __init__(self, storage: TeamStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

        self._bus.register_handler(TeamCreatedEvent, self._handle_team_created)

    def close(self) -> None:
        self._bus.unregister_handler(TeamCreatedEvent, self._handle_team_created)

    def get(self, id_: TeamID) -> Optional[Team]:
        dto = self._storage.get(id_.value)
        return self._to_team(dto) if dto is not None else None

    def find(self, name: str) -> Optional[Team]:
        dto = self._storage.find(name)
        return self._to_team(dto) if dto is not None else None

    def all_(self) -> List[Team]:
        dtos = self._storage.all_()
        return [self._to_team(dto) for dto in dtos if dto is not None]

    def _to_team(self, dto: TeamDto) -> Team:
        return Team(self._bus, TeamID(dto.id_), dto.name)

    def _handle_team_created(self, event: TeamCreatedEvent) -> None:
        self._storage.add(TeamDto(event.id_, event.name))

    def __enter__(self) -> "TeamRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

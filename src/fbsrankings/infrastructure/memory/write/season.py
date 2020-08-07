from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.memory.storage import SeasonDto
from fbsrankings.infrastructure.memory.storage import SeasonStorage


class SeasonRepository(BaseRepository):
    def __init__(self, storage: SeasonStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, id_: SeasonID) -> Optional[Season]:
        dto = self._storage.get(id_.value)
        return self._to_season(dto) if dto is not None else None

    def find(self, year: int) -> Optional[Season]:
        dto = self._storage.find(year)
        return self._to_season(dto) if dto is not None else None

    def all(self) -> List[Season]:
        dtos = self._storage.all()
        return [self._to_season(dto) for dto in dtos if dto is not None]

    def _to_season(self, dto: SeasonDto) -> Season:
        return Season(self._bus, SeasonID(dto.id_), dto.year)

    def handle(self, event: Event) -> bool:
        if isinstance(event, SeasonCreatedEvent):
            self._handle_season_created(event)
            return True
        return False

    def _handle_season_created(self, event: SeasonCreatedEvent) -> None:
        self._storage.add(SeasonDto(event.id_, event.year))

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

    def get(self, ID: SeasonID) -> Optional[Season]:
        return self._to_season(self._storage.get(ID.value))

    def find(self, year: int) -> Optional[Season]:
        return self._to_season(self._storage.find(year))

    def _to_season(self, dto: Optional[SeasonDto]) -> Optional[Season]:
        if dto is not None:
            return Season(self._bus, SeasonID(dto.ID), dto.year)
        return None

    def handle(self, event: Event) -> bool:
        if isinstance(event, SeasonCreatedEvent):
            self._handle_season_created(event)
            return True
        else:
            return False

    def _handle_season_created(self, event: SeasonCreatedEvent) -> None:
        self._storage.add(SeasonDto(event.ID, event.year))

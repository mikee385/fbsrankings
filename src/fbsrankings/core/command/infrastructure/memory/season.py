from typing import Optional

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.season import (
    SeasonRepository as BaseRepository,
)
from fbsrankings.messages.event import SeasonCreatedEvent
from fbsrankings.messages.event import SeasonEventHandler as BaseEventHandler
from fbsrankings.storage.memory import SeasonDto
from fbsrankings.storage.memory import SeasonStorage


class SeasonRepository(BaseRepository):
    def __init__(self, storage: SeasonStorage, bus: EventBus) -> None:
        self._storage = storage
        self._bus = bus

    def get(self, id_: SeasonID) -> Optional[Season]:
        dto = self._storage.get(id_)
        return self._to_season(dto) if dto is not None else None

    def find(self, year: int) -> Optional[Season]:
        dto = self._storage.find(year)
        return self._to_season(dto) if dto is not None else None

    def _to_season(self, dto: SeasonDto) -> Season:
        return Season(self._bus, SeasonID(dto.id_), dto.year)


class SeasonEventHandler(BaseEventHandler):
    def __init__(self, storage: SeasonStorage) -> None:
        self._storage = storage

    def handle_created(self, event: SeasonCreatedEvent) -> None:
        self._storage.add(SeasonDto(event.id_, event.year))

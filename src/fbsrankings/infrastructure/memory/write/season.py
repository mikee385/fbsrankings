from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.memory.storage import SeasonDto
from fbsrankings.infrastructure.memory.storage import SeasonStorage


class SeasonRepository(BaseRepository, ContextManager["SeasonRepository"]):
    def __init__(self, storage: SeasonStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

        self._bus.register_handler(SeasonCreatedEvent, self._handle_season_created)

    def close(self) -> None:
        self._bus.unregister_handler(SeasonCreatedEvent, self._handle_season_created)

    def get(self, id_: SeasonID) -> Optional[Season]:
        dto = self._storage.get(id_.value)
        return self._to_season(dto) if dto is not None else None

    def find(self, year: int) -> Optional[Season]:
        dto = self._storage.find(year)
        return self._to_season(dto) if dto is not None else None

    def _to_season(self, dto: SeasonDto) -> Season:
        return Season(self._bus, SeasonID(dto.id_), dto.year)

    def _handle_season_created(self, event: SeasonCreatedEvent) -> None:
        self._storage.add(SeasonDto(event.id_, event.year))

    def __enter__(self) -> "SeasonRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

from typing import Optional

from fbsrankings.common import EventBus
from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationEventHandler as BaseEventHandler
from fbsrankings.domain import AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import SeasonID
from fbsrankings.domain import Subdivision
from fbsrankings.domain import TeamID
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.infrastructure.memory.storage import AffiliationDto
from fbsrankings.infrastructure.memory.storage import AffiliationStorage


class AffiliationRepository(BaseRepository):
    def __init__(self, storage: AffiliationStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        dto = self._storage.get(id_.value)
        return self._to_affiliation(dto) if dto is not None else None

    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        dto = self._storage.find(season_id.value, team_id.value)
        return self._to_affiliation(dto) if dto is not None else None

    def _to_affiliation(self, dto: AffiliationDto) -> Affiliation:
        return Affiliation(
            self._bus,
            AffiliationID(dto.id_),
            SeasonID(dto.season_id),
            TeamID(dto.team_id),
            Subdivision[dto.subdivision],
        )


class AffiliationEventHandler(BaseEventHandler):
    def __init__(self, storage: AffiliationStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        self._storage.add(
            AffiliationDto(
                event.id_,
                event.season_id,
                event.team_id,
                event.subdivision,
            ),
        )

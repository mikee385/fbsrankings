from typing import Optional

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.affiliation import (
    AffiliationEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.affiliation import AffiliationID
from fbsrankings.core.command.domain.model.affiliation import (
    AffiliationRepository as BaseRepository,
)
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.event.affiliation import AffiliationCreatedEvent
from fbsrankings.enum import Subdivision
from fbsrankings.storage.memory import AffiliationDto
from fbsrankings.storage.memory import AffiliationStorage


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

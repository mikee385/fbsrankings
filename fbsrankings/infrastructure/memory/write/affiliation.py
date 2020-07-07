from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Affiliation
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

    def get(self, ID: AffiliationID) -> Optional[Affiliation]:
        dto = self._storage.get(ID.value)
        return self._to_affiliation(dto) if dto is not None else None

    def find(self, season_ID: SeasonID, team_ID: TeamID) -> Optional[Affiliation]:
        dto = self._storage.find(season_ID.value, team_ID.value)
        return self._to_affiliation(dto) if dto is not None else None

    def for_season(self, season_ID: SeasonID) -> List[Affiliation]:
        dtos = self._storage.for_season(season_ID.value)
        return [self._to_affiliation(dto) for dto in dtos if dto is not None]

    def _to_affiliation(self, dto: AffiliationDto) -> Affiliation:
        return Affiliation(
            self._bus,
            AffiliationID(dto.ID),
            SeasonID(dto.season_ID),
            TeamID(dto.team_ID),
            Subdivision[dto.subdivision],
        )

    def handle(self, event: Event) -> bool:
        if isinstance(event, AffiliationCreatedEvent):
            self._handle_affiliation_created(event)
            return True
        else:
            return False

    def _handle_affiliation_created(self, event: AffiliationCreatedEvent) -> None:
        self._storage.add(
            AffiliationDto(event.ID, event.season_ID, event.team_ID, event.subdivision)
        )

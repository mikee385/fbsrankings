from typing import Optional
from typing import Union

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationID
from fbsrankings.domain import AffiliationRepository as BaseRepository
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import Subdivision
from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.infrastructure.memory.storage import AffiliationDto
from fbsrankings.infrastructure.memory.storage import AffiliationStorage


class AffiliationRepository(BaseRepository):
    def __init__(self, storage: AffiliationStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, ID: AffiliationID) -> Optional[Affiliation]:
        return self._to_affiliation(self._storage.get(ID.value))

    def find(
        self, season: Union[Season, SeasonID], team: Union[Team, TeamID]
    ) -> Optional[Affiliation]:
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError("season must be of type Season or SeasonID")

        if isinstance(team, Team):
            team_ID = team.ID
        elif isinstance(team, TeamID):
            team_ID = team
        else:
            raise TypeError("team must be of type Team or TeamID")

        return self._to_affiliation(self._storage.find(season_ID.value, team_ID.value))

    def _to_affiliation(self, dto: Optional[AffiliationDto]) -> Optional[Affiliation]:
        if dto is not None:
            return Affiliation(
                self._bus,
                AffiliationID(dto.ID),
                SeasonID(dto.season_ID),
                TeamID(dto.team_ID),
                Subdivision[dto.subdivision],
            )
        return None

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

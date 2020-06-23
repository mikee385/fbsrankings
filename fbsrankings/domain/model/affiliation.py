from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from fbsrankings.common import EventBus, Identifier
from fbsrankings.domain.model.season import Season, SeasonID
from fbsrankings.domain.model.team import Team, TeamID
from fbsrankings.event import AffiliationCreatedEvent


class Subdivision(Enum):
    FBS = 1
    FCS = 2


class AffiliationID(Identifier):
    pass


class Affiliation(object):
    def __init__(
        self,
        bus: EventBus,
        ID: AffiliationID,
        season: Union[Season, SeasonID],
        team: Union[Team, TeamID],
        subdivision: Subdivision,
    ) -> None:
        self._bus = bus
        self._ID = ID

        if isinstance(season, Season):
            self._season_ID = season.ID
        elif isinstance(season, SeasonID):
            self._season_ID = season
        else:
            raise TypeError("season must be of type Season or SeasonID")

        if isinstance(team, Team):
            self._team_ID = team.ID
        elif isinstance(team, TeamID):
            self._team_ID = team
        else:
            raise TypeError("team must be of type Team or TeamID")

        self._subdivision = subdivision

    @property
    def ID(self) -> AffiliationID:
        return self._ID

    @property
    def season_ID(self) -> SeasonID:
        return self._season_ID

    @property
    def team_ID(self) -> TeamID:
        return self._team_ID

    @property
    def subdivision(self) -> Subdivision:
        return self._subdivision


class AffiliationRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self, season: SeasonID, team: TeamID, subdivision: Subdivision
    ) -> Affiliation:
        ID = AffiliationID(uuid4())
        affiliation = Affiliation(self._bus, ID, season, team, subdivision)
        self._bus.publish(
            AffiliationCreatedEvent(
                affiliation.ID.value,
                affiliation.season_ID.value,
                affiliation.team_ID.value,
                affiliation.subdivision.name,
            )
        )

        return affiliation

    @abstractmethod
    def get(self, ID: AffiliationID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season: SeasonID, team: TeamID) -> Optional[Affiliation]:
        raise NotImplementedError

from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from typing import List
from typing import Optional
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import TeamID
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
        season_ID: SeasonID,
        team_ID: TeamID,
        subdivision: Subdivision,
    ) -> None:
        self._bus = bus
        self._ID = ID
        self._season_ID = season_ID
        self._team_ID = team_ID
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
        self, season_ID: SeasonID, team_ID: TeamID, subdivision: Subdivision,
    ) -> Affiliation:
        ID = AffiliationID(uuid4())
        affiliation = Affiliation(self._bus, ID, season_ID, team_ID, subdivision)
        self._bus.publish(
            AffiliationCreatedEvent(
                affiliation.ID.value,
                affiliation.season_ID.value,
                affiliation.team_ID.value,
                affiliation.subdivision.name,
            ),
        )

        return affiliation

    @abstractmethod
    def get(self, ID: AffiliationID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season: SeasonID, team_ID: TeamID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def for_season(self, season_ID: SeasonID) -> List[Affiliation]:
        raise NotImplementedError

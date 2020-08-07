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


class Affiliation:
    def __init__(
        self,
        bus: EventBus,
        id_: AffiliationID,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> None:
        self._bus = bus
        self._id = id_
        self._season_id = season_id
        self._team_id = team_id
        self._subdivision = subdivision

    @property
    def id_(self) -> AffiliationID:
        return self._id

    @property
    def season_id(self) -> SeasonID:
        return self._season_id

    @property
    def team_id(self) -> TeamID:
        return self._team_id

    @property
    def subdivision(self) -> Subdivision:
        return self._subdivision


class AffiliationRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self, season_id: SeasonID, team_id: TeamID, subdivision: Subdivision,
    ) -> Affiliation:
        id_ = AffiliationID(uuid4())
        affiliation = Affiliation(self._bus, id_, season_id, team_id, subdivision)
        self._bus.publish(
            AffiliationCreatedEvent(
                affiliation.id_.value,
                affiliation.season_id.value,
                affiliation.team_id.value,
                affiliation.subdivision.name,
            ),
        )

        return affiliation

    @abstractmethod
    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def for_season(self, season_id: SeasonID) -> List[Affiliation]:
        raise NotImplementedError

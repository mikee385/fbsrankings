from abc import ABCMeta
from abc import abstractmethod
from typing import NewType
from typing import Optional
from uuid import UUID
from uuid import uuid4

from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.shared.enums import Subdivision
from fbsrankings.shared.event import AffiliationCreatedEvent
from fbsrankings.shared.messaging import EventBus


AffiliationID = NewType("AffiliationID", UUID)


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


class AffiliationFactory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        id_ = AffiliationID(uuid4())
        affiliation = Affiliation(self._bus, id_, season_id, team_id, subdivision)
        self._bus.publish(
            AffiliationCreatedEvent(
                affiliation.id_,
                affiliation.season_id,
                affiliation.team_id,
                affiliation.subdivision.name,
            ),
        )

        return affiliation


class AffiliationRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        raise NotImplementedError

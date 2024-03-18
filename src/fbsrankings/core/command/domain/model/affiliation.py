from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import NewType
from typing import Optional
from typing import Type
from uuid import UUID
from uuid import uuid4

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.event.affiliation import AffiliationCreatedEvent
from fbsrankings.enum import Subdivision


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


class AffiliationRepository(metaclass=ABCMeta):
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

    @abstractmethod
    def get(self, id_: AffiliationID) -> Optional[Affiliation]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season_id: SeasonID, team_id: TeamID) -> Optional[Affiliation]:
        raise NotImplementedError


class AffiliationEventHandler(
    ContextManager["AffiliationEventHandler"],
    metaclass=ABCMeta,
):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._bus.register_handler(AffiliationCreatedEvent, self.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(AffiliationCreatedEvent, self.handle_created)

    @abstractmethod
    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        raise NotImplementedError

    def __enter__(self) -> "AffiliationEventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

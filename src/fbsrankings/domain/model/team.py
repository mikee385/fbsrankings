from abc import ABCMeta
from abc import abstractmethod
from typing import List
from typing import Optional
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.event import TeamCreatedEvent


class TeamID(Identifier):
    pass


class Team:
    def __init__(self, bus: EventBus, id_: TeamID, name: str) -> None:
        self._bus = bus
        self._id = id_
        self._name = name

    @property
    def id_(self) -> TeamID:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class TeamRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, name: str) -> Team:
        id_ = TeamID(uuid4())
        team = Team(self._bus, id_, name)
        self._bus.publish(TeamCreatedEvent(team.id_.value, team.name))

        return team

    @abstractmethod
    def get(self, id_: TeamID) -> Optional[Team]:
        raise NotImplementedError

    @abstractmethod
    def find(self, name: str) -> Optional[Team]:
        raise NotImplementedError

    @abstractmethod
    def all_(self) -> List[Team]:
        raise NotImplementedError

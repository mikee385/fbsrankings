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


class Team(object):
    def __init__(self, bus: EventBus, id: TeamID, name: str) -> None:
        self._bus = bus
        self._id = id
        self._name = name

    @property
    def id(self) -> TeamID:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class TeamRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, name: str) -> Team:
        id = TeamID(uuid4())
        team = Team(self._bus, id, name)
        self._bus.publish(TeamCreatedEvent(team.id.value, team.name))

        return team

    @abstractmethod
    def get(self, id: TeamID) -> Optional[Team]:
        raise NotImplementedError

    @abstractmethod
    def find(self, name: str) -> Optional[Team]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List[Team]:
        raise NotImplementedError

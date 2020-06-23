from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import uuid4

from fbsrankings.common import EventBus, Identifier
from fbsrankings.event import TeamCreatedEvent


class TeamID(Identifier):
    pass


class Team(object):
    def __init__(self, bus: EventBus, ID: TeamID, name: str) -> None:
        self._bus = bus
        self._ID = ID
        self._name = name

    @property
    def ID(self) -> TeamID:
        return self._ID

    @property
    def name(self) -> str:
        return self._name


class TeamRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, name: str) -> Team:
        ID = TeamID(uuid4())
        team = Team(self._bus, ID, name)
        self._bus.publish(TeamCreatedEvent(team.ID.value, team.name))

        return team

    @abstractmethod
    def get(self, ID: TeamID) -> Optional[Team]:
        raise NotImplementedError

    @abstractmethod
    def find(self, name: str) -> Optional[Team]:
        raise NotImplementedError

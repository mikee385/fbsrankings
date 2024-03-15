from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from uuid import uuid4

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.core.command.event.team import TeamCreatedEvent


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


class TeamEventHandler(ContextManager["TeamEventHandler"], metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._bus.register_handler(TeamCreatedEvent, self.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(TeamCreatedEvent, self.handle_created)

    @abstractmethod
    def handle_created(self, event: TeamCreatedEvent) -> None:
        raise NotImplementedError

    def __enter__(self) -> "TeamEventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

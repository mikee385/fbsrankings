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
from fbsrankings.core.command.event.season import SeasonCreatedEvent


class SeasonID(Identifier):
    pass


class Season:
    def __init__(self, bus: EventBus, id_: SeasonID, year: int) -> None:
        self._bus = bus
        self._id = id_
        self._year = year

    @property
    def id_(self) -> SeasonID:
        return self._id

    @property
    def year(self) -> int:
        return self._year


class SeasonRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, year: int) -> Season:
        id_ = SeasonID(uuid4())
        season = Season(self._bus, id_, year)
        self._bus.publish(SeasonCreatedEvent(season.id_.value, season.year))

        return season

    @abstractmethod
    def get(self, id_: SeasonID) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def find(self, year: int) -> Optional[Season]:
        raise NotImplementedError


class SeasonEventHandler(ContextManager["SeasonEventHandler"], metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._bus.register_handler(SeasonCreatedEvent, self.handle_created)

    def close(self) -> None:
        self._bus.unregister_handler(SeasonCreatedEvent, self.handle_created)

    @abstractmethod
    def handle_created(self, event: SeasonCreatedEvent) -> None:
        raise NotImplementedError

    def __enter__(self) -> "SeasonEventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

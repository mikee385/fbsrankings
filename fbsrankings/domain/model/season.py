from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from typing import List
from typing import Optional
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.event import SeasonCreatedEvent


class SeasonSection(Enum):
    PRESEASON = 0
    REGULAR_SEASON = 1
    POSTSEASON = 2


class SeasonID(Identifier):
    pass


class Season:
    def __init__(self, bus: EventBus, id: SeasonID, year: int) -> None:
        self._bus = bus
        self._id = id
        self._year = year

    @property
    def id(self) -> SeasonID:
        return self._id

    @property
    def year(self) -> int:
        return self._year


class SeasonRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, year: int) -> Season:
        id = SeasonID(uuid4())
        season = Season(self._bus, id, year)
        self._bus.publish(SeasonCreatedEvent(season.id.value, season.year))

        return season

    @abstractmethod
    def get(self, id: SeasonID) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def find(self, year: int) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List[Season]:
        raise NotImplementedError

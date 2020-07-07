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


class Season(object):
    def __init__(self, bus: EventBus, ID: SeasonID, year: int) -> None:
        self._bus = bus
        self._ID = ID
        self._year = year

    @property
    def ID(self) -> SeasonID:
        return self._ID

    @property
    def year(self) -> int:
        return self._year


class SeasonRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, year: int) -> Season:
        ID = SeasonID(uuid4())
        season = Season(self._bus, ID, year)
        self._bus.publish(SeasonCreatedEvent(season.ID.value, season.year))

        return season

    @abstractmethod
    def get(self, ID: SeasonID) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def find(self, year: int) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List[Season]:
        raise NotImplementedError

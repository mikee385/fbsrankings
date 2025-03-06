from abc import ABCMeta
from abc import abstractmethod
from typing import NewType
from typing import Optional
from uuid import UUID
from uuid import uuid4

from communication.bus import EventBus
from fbsrankings.messages.event import SeasonCreatedEvent


SeasonID = NewType("SeasonID", UUID)


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


class SeasonFactory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(self, year: int) -> Season:
        id_ = SeasonID(uuid4())
        season = Season(self._bus, id_, year)
        self._bus.publish(SeasonCreatedEvent(uuid4(), season.id_, season.year))

        return season


class SeasonRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, id_: SeasonID) -> Optional[Season]:
        raise NotImplementedError

    @abstractmethod
    def find(self, year: int) -> Optional[Season]:
        raise NotImplementedError

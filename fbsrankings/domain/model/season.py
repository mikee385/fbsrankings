from uuid import uuid4
from enum import Enum

from fbsrankings.common import Identifier, EventBus
from fbsrankings.event import SeasonRegisteredEvent


class SeasonSection (Enum):
    PRESEASON = 0
    REGULAR_SEASON = 1
    POSTSEASON = 2


class SeasonID (Identifier):
    pass


class Season (object):
    def __init__(self, bus, ID, year):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        self._ID = ID
        
        self._year = year
        
    @property
    def ID(self):
        return self._ID
        
    @property
    def year(self):
        return self._year


class SeasonRepository (object):
    def __init__(self, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        
    def register(self, year):
        ID = SeasonID(uuid4())
        season = Season(self._bus, ID, year)
        self._bus.publish(SeasonRegisteredEvent(season.ID, season.year))
        
        return season
        
    def find_by_ID(self, ID):
        raise NotImplementedError
        
    def find_by_year(self, year):
        raise NotImplementedError
        
    def all(self):
        raise NotImplementedError

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
    def __init__(self, event_bus, ID, year):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
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
    @property
    def event_bus(self):
        raise NotImplementedError
        
    def find_by_ID(self, ID):
        raise NotImplementedError
        
    def find_by_year(self, year):
        raise NotImplementedError
        
    def all(self):
        raise NotImplementedError
        

class SeasonManager (SeasonRepository):
    def __init__(self, repository):
        if not isinstance(repository, SeasonRepository):
            raise TypeError('repository must be of type SeasonRepository')
        self._repository = repository
        
    @property
    def event_bus(self):
        return self._repository.event_bus
   
    def register(self, year):
        ID = SeasonID(uuid4())
        season = Season(self.event_bus, ID, year)
        self.event_bus.raise_event(SeasonRegisteredEvent(season.ID, season.year))
        
        return season
        
    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_year(self, year):
        return self._repository.find_by_year(year)
        
    def all(self):
        return self._repository.all()

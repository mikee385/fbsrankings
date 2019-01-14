from uuid import uuid4
from enum import Enum

from fbsrankings.common import Identifier, Event, EventBus


class SeasonSection (Enum):
    PRESEASON = 0
    REGULAR_SEASON = 1
    CONFERENCE_CHAMPIONSHIP = 2
    POSTSEASON = 3


class SeasonID (Identifier):
    pass


class Season (object):
    def __init__(self, event_bus, ID, year):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        self.ID = ID
        
        self.year = year


class SeasonFactory (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._event_bus.register_type(SeasonRegisteredEvent)
        
    def new_season(self, year):
        ID = SeasonID(uuid4())
        season = Season(self._event_bus, ID, year)
        season._event_bus.raise_event(SeasonRegisteredEvent(season.ID, season.year))
        
        return season


class SeasonRepository (object):
    def add_season(self, season):
        raise NotImplementedError

    def find_season(self, ID):
        raise NotImplementedError
        
    def find_season_by_year(self, year):
        raise NotImplementedError
        
    def all_seasons(self):
        raise NotImplementedError
        

class SeasonRegisteredEvent (Event):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year

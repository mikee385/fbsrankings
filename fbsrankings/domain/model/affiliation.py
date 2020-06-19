from uuid import uuid4
from enum import Enum

from fbsrankings.common import Identifier, EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID
from fbsrankings.event import AffiliationCreatedEvent


class Subdivision (Enum):
    FBS = 1
    FCS = 2


class AffiliationID (Identifier):
    pass


class Affiliation (object):
    def __init__(self, bus, ID, season, team, subdivision):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        
        if not isinstance(ID, AffiliationID):
            raise TypeError('ID must be of type AffiliationID')
        self._ID = ID
        
        if isinstance(season, Season):
            self._season_ID = season.ID
        elif isinstance(season, SeasonID):
            self._season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team, Team):
            self._team_ID = team.ID
        elif isinstance(team, TeamID):
            self._team_ID = team
        else:
            raise TypeError('team must be of type Team or TeamID')
        
        if not isinstance(subdivision, Subdivision):
            raise TypeError('subdivision must be of type Subdivision')
        self._subdivision = subdivision
        
    @property
    def ID(self):
        return self._ID
        
    @property
    def season_ID(self):
        return self._season_ID
        
    @property
    def team_ID(self):
        return self._team_ID
        
    @property
    def subdivision(self):
        return self._subdivision


class AffiliationRepository (object):
    def __init__(self, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
    
    def create(self, season, team, subdivision):
        ID = AffiliationID(uuid4())
        affiliation = Affiliation(self._bus, ID, season, team, subdivision)
        self._bus.publish(AffiliationCreatedEvent(affiliation.ID, affiliation.season_ID, affiliation.team_ID, affiliation.subdivision))
        
        return affiliation

    def get(self, ID):
        raise NotImplementedError
        
    def find(self, season, team):
        raise NotImplementedError

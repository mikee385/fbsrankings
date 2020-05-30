from uuid import uuid4
from enum import Enum

from fbsrankings.common import Identifier, EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID
from fbsrankings.event import AffiliationRegisteredEvent


class Subdivision (Enum):
    FBS = 1
    FCS = 2


class AffiliationID (Identifier):
    pass


class Affiliation (object):
    def __init__(self, event_bus, ID, season, team, subdivision):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
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
    @property
    def event_bus(self):
        raise NotImplementedError

    def find_by_ID(self, ID):
        raise NotImplementedError
        
    def find_by_season_team(self, season, team):
        raise NotImplementedError
        
    def find_by_season(self, season):
        raise NotImplementedError
        

class AffiliationManager (AffiliationRepository):
    def __init__(self, repository):
        if not isinstance(repository, AffiliationRepository):
            raise TypeError('event_bus must be of type AffiliationRepository')
        self._repository = repository
        
    @property
    def event_bus(self):
        return self._repository.event_bus

    def register(self, season, team, subdivision):
        ID = AffiliationID(uuid4())
        affiliation = Affiliation(self.event_bus, ID, season, team, subdivision)
        self.event_bus.raise_event(AffiliationRegisteredEvent(affiliation.ID, affiliation.season_ID, affiliation.team_ID, affiliation.subdivision))
        
        return affiliation
        
    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_season_team(self, season, team):
        return self._repository.find_by_season_team(season, team)
        
    def find_by_season(self, season):
        return self._repository.find_by_season(season)

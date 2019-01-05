from uuid import uuid4
from enum import Enum

from fbsrankings.common import Identifier, Event, EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID


class Subdivision(Enum):
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
        self.ID = ID
        
        if isinstance(season, Season):
            self.season_ID = season.ID
        elif isinstance(season, SeasonID):
            self.season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team, Team):
            self.team_ID = team.ID
        elif isinstance(team, TeamID):
            self.team_ID = team
        else:
            raise TypeError('team must be of type Team or TeamID')
        
        if not isinstance(subdivision, Subdivision):
            raise TypeError('subdivision must be of type Subdivision')
        self.subdivision = subdivision


class AffiliationFactory (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._event_bus.register_type(AffiliationRegisteredEvent)
        
    def new_affiliation(self, season, team, subdivision):
        ID = AffiliationID(uuid4())
        affiliation = Affiliation(self._event_bus, ID, season, team, subdivision)
        affiliation._event_bus.raise_event(AffiliationRegisteredEvent(affiliation.ID, affiliation.season_ID, affiliation.team_ID, affiliation.subdivision))
        
        return affiliation


class AffiliationRepository (object):
    def add_affiliation(self, affiliation):
        raise NotImplementedError

    def find_affiliation(self, ID):
        raise NotImplementedError
        
    def find_affiliation_by_season_team(self, season, team):
        raise NotImplementedError
        
    def find_affiliations_by_season(self, season):
        raise NotImplementedError


class AffiliationRegisteredEvent (Event):
    def __init__(self, ID, season_ID, team_ID, subdivision):
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision

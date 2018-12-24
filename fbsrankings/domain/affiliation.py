from enum import Enum

from fbsrankings.common.identifier import Identifier
from fbsrankings.domain.season import Season, SeasonID
from fbsrankings.domain.team import Team, TeamID


class Subdivision(Enum):
    FBS = 1
    FCS = 2


class AffiliationID (Identifier):
    pass


class Affiliation (object):
    def __init__(self, ID, season, team, subdivision):
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


class AffiliationRepository (object):
    def AddAffiliation(self, season, team, *args, **kwargs):
        pass

    def FindAffiliation(self, ID):
        pass
        
    def FindAffiliationBySeasonTeam(self, season, team):
        pass
        
    def FindAffiliationsBySeason(self, season):
        pass
    

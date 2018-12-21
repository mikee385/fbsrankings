from uuid import uuid4
from fbsrankings.domain.affiliation import Affiliation, AffiliationID, AffiliationRepository as BaseRepository
from fbsrankings.domain.season import Season, SeasonID
from fbsrankings.domain.team import Team, TeamID


class AffiliationRepository (BaseRepository):
    def __init__(self):
        self._affiliation_id_dict = {}
        self._affiliation_season_dict = {}
    
    def AddAffiliation(self, season, team, *args, **kwargs):
        ID = AffiliationID(uuid4())
        value = Affiliation(ID, season, team, *args, **kwargs)
        
        self._affiliation_id_dict[ID] = value
        
        season_dict = self._affiliation_season_dict.get(value.season_ID)
        if season_dict is None:
            season_dict = {}
            self._affiliation_season_dict[value.season_ID] = season_dict
        season_dict[value.team_ID] = value
        
        return value

    def FindAffiliation(self, ID):
        if not isinstance(ID, AffiliationID):
            raise TypeError('ID must be of type AffiliationID')
        return self._affiliation_id_dict.get(ID)
        
    def FindAffiliationBySeasonTeam(self, season, team):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team, Team):
            team_ID = team.ID
        elif isinstance(team, TeamID):
            team_ID = team
        else:
            raise TypeError('team must be of type Team or TeamID')
            
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return season_dict.get(team_ID)
        
    def FindAffiliationsBySeason(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
        
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return list(season_dict.values())
    
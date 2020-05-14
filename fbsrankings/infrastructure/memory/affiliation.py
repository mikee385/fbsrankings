from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationRepository as BaseRepository
from fbsrankings.event import AffiliationRegisteredEvent


class AffiliationDto (object):
    def __init__(self, ID, season_ID, team_ID, subdivision):
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision


class AffiliationDataStore (object):
    def __init__(self):
        self._affiliation_id_dict = {}
        self._affiliation_season_dict = {}
    
    def add(self, affiliation):
        if not isinstance(affiliation, AffiliationDto):
            raise TypeError('affiliation must be of type AffiliationDto')
        
        season_dict = self._affiliation_season_dict.get(affiliation.season_ID)
        if season_dict is None:
            season_dict = {}
            self._affiliation_season_dict[affiliation.season_ID] = season_dict
        elif affiliation.team_ID in season_dict:
            raise ValueError(f'Affiliation already exists for team {affiliation.team_ID} in season {affiliation.season_ID}')
        season_dict[affiliation.team_ID] = affiliation
        self._affiliation_id_dict[affiliation.ID] = affiliation

    def find_by_ID(self, ID):
        return self._affiliation_id_dict.get(ID)
        
    def find_by_season_team(self, season_ID, team_ID):
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return season_dict.get(team_ID)
        
    def find_by_season(self, season_ID):
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return []
        return [item for item in season_dict.values()]
        

class AffiliationRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, AffiliationDataStore):
            raise TypeError('data_store must be of type AffiliationDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def _to_affiliation(self, dto):
        if dto is not None:
            return Affiliation(self._event_bus, dto.ID, dto.season_ID, dto.team_ID, dto.subdivision)
        return None

    def find_by_ID(self, ID):
        return self._to_affiliation(self._data_store.find_by_ID(ID))
        
    def find_by_season_team(self, season, team):
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
            
        return self._to_affiliation(self._data_store.find_by_season_team(season_ID, team_ID))
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        return [self._to_affiliation(item) for item in self._data_store.find_by_season(season_ID)]
        
    def try_handle_event(self, event):
        if isinstance(event, AffiliationRegisteredEvent):
            self._data_store.add(AffiliationDto(event.ID, event.season_ID, event.team_ID, event.subdivision))
            return True
        else:
            return False

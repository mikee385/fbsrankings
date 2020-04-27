from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationID, AffiliationRepository as BaseRepository, AffiliationRegisteredEvent


class AffiliationDataStore (BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._affiliation_id_dict = {}
        self._affiliation_season_dict = {}
    
    def add(self, affiliation):
        if not isinstance(affiliation, Affiliation):
            raise TypeError('affiliation must be of type Affiliation')
            
        affiliation = affiliation.copy(self._event_bus)
        self._affiliation_id_dict[affiliation.ID] = affiliation
        
        season_dict = self._affiliation_season_dict.get(affiliation.season_ID)
        if season_dict is None:
            season_dict = {}
            self._affiliation_season_dict[affiliation.season_ID] = season_dict
        season_dict[affiliation.team_ID] = affiliation

    def find_by_ID(self, ID):
        if not isinstance(ID, AffiliationID):
            raise TypeError('ID must be of type AffiliationID')
        return self._affiliation_id_dict.get(ID)
        
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
            
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return season_dict.get(team_ID)
        
    def find_by_season(self, season):
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
        

class AffiliationRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, AffiliationDataStore):
            raise TypeError('data_store must be of type AffiliationDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus

    def find_by_ID(self, ID):
        return self._copy(self._data_store.find_by_ID(ID))
        
    def find_by_season_team(self, season, team):
        return self._copy(self._data_store.find_by_season_team(season, team))
        
    def find_by_season(self, season):
        return [self._copy(item) for item in self._data_store.find_by_season(season)]
        
    def _copy(self, affiliation):
        return affiliation.copy(self._event_bus) if affiliation is not None else None
        
    def try_handle_event(self, event):
        if isinstance(event, AffiliationRegisteredEvent):
            self._data_store.add(Affiliation(self._event_bus, event.ID, event.season_ID, event.team_ID, event.subdivision))
            return True
        else:
            return False

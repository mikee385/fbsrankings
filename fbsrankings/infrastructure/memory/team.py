from fbsrankings.common import EventBus
from fbsrankings.domain import Team, TeamRepository as BaseRepository
from fbsrankings.event import TeamRegisteredEvent


class TeamDto (object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name


class TeamDataStore (object):
    def __init__(self):
        self._team_id_dict = {}
        self._team_name_dict = {}
    
    def add(self, team):
        if not isinstance(team, TeamDto):
            raise TypeError('team must be of type TeamDto')
            
        if team.name in self._team_name_dict:
            raise ValueError(f'Team already exists for name {team.name}')
            
        self._team_id_dict[team.ID] = team
        self._team_name_dict[team.name] = team

    def find_by_ID(self, ID):
        return self._team_id_dict.get(ID)
        
    def find_by_name(self, name):
        return self._team_name_dict.get(name)
        
    def all(self):
        return [item for item in self._team_name_dict.values()]
        

class TeamRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, TeamDataStore):
            raise TypeError('data_store must be of type TeamDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def _to_team(self, dto):
        if dto is not None:
            return Team(self._event_bus, dto.ID, dto.name)
        return None

    def find_by_ID(self, ID):
        return self._to_team(self._data_store.find_by_ID(ID))
        
    def find_by_name(self, name):
        return self._to_team(self._data_store.find_by_name(name))
        
    def all(self):
        return [self._to_team(item) for item in self._data_store.all()]
        
    def try_handle_event(self, event):
        if isinstance(event, TeamRegisteredEvent):
            self._data_store.add(TeamDto(event.ID, event.name))
            return True
        else:
            return False

from fbsrankings.common import EventBus
from fbsrankings.domain import Team, TeamID, TeamRepository as BaseRepository, TeamRegisteredEvent


class TeamDataStore (BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._team_id_dict = {}
        self._team_name_dict = {}
    
    def add(self, team):
        if not isinstance(team, Team):
            raise TypeError('team must be of type Team')
            
        if team.name in self._team_name_dict:
            raise ValueError(f'Team already exists for name {team.name}')
            
        team = team.copy(self._event_bus)
            
        self._team_id_dict[team.ID] = team
        self._team_name_dict[team.name] = team

    def find_by_ID(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        return self._team_id_dict.get(ID)
        
    def find_by_name(self, name):
        return self._team_name_dict.get(name)
        
    def all(self):
        return self._team_name_dict.values()
        

class TeamRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, TeamDataStore):
            raise TypeError('data_store must be of type TeamDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def add(self, team):
        # Handled through events
        pass

    def find_by_ID(self, ID):
        return self._copy(self._data_store.find_by_ID(ID))
        
    def find_by_name(self, name):
        return self._copy(self._data_store.find_by_name(name))
        
    def all(self):
        return [self._copy(item) for item in self._data_store.all()]
        
    def _copy(self, team):
        return team.copy(self._event_bus) if team is not None else None
        
    def try_handle_event(self, event):
        if isinstance(event, TeamRegisteredEvent):
            self._data_store.add(Team(self._event_bus, event.ID, event.name))
            return True
        else:
            return False

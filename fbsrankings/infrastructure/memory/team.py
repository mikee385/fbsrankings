from fbsrankings.common import EventBus
from fbsrankings.domain import Team, TeamRepository
from fbsrankings.event import TeamRegisteredEvent


class TeamDto (object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name


class TeamDataSource (object):
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
        

class TeamQueryHandler (TeamRepository):
    def __init__(self, data_source, event_bus):
        super().__init__(event_bus)
        
        if not isinstance(data_source, TeamDataSource):
            raise TypeError('repository must be of type TeamDataSource')
        self._data_source = data_source
        
    def _to_team(self, dto):
        if dto is not None:
            return Team(self._event_bus, dto.ID, dto.name)
        return None

    def find_by_ID(self, ID):
        return self._to_team(self._data_source.find_by_ID(ID))
        
    def find_by_name(self, name):
        return self._to_team(self._data_source.find_by_name(name))
        
    def all(self):
        return [self._to_team(item) for item in self._data_source.all()]
        
        
class TeamEventHandler (object):
    def __init__(self, data_source, event_bus):
        if not isinstance(data_source, TeamDataSource):
            raise TypeError('data_source must be of type TeamDataSource')
        self._data_source = data_source
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def handle(self, event):
        if isinstance(event, TeamRegisteredEvent):
            self._handle_team_registered(event)
            return True
        else:
            return False
        
    def _handle_team_registered(self, event):
        self._data_source.add(TeamDto(event.ID, event.name))

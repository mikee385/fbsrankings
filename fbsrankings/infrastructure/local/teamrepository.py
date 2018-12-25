from uuid import uuid4

from fbsrankings.domain.team import Team, TeamID, TeamRepository as BaseRepository


class TeamRepository(BaseRepository):
    def __init__(self):
        self._team_id_dict = {}
        self._team_name_dict = {}
    
    def add_team(self, name, *args, **kwargs):
        if name in self._team_name_dict:
            raise ValueError('Team already exists for name ' + str(name))
            
        ID = TeamID(uuid4())
        value = Team(ID, name, *args, **kwargs)
        
        self._team_id_dict[ID] = value
        self._team_name_dict[name] = value
        
        return value

    def find_team(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        return self._team_id_dict.get(ID)
        
    def find_team_by_name(self, name):
        return self._team_name_dict.get(name)
        
    def all_teams(self):
        return self._team_name_dict.values()

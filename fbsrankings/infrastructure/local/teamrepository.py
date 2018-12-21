from uuid import uuid4
from fbsrankings.domain.team import Team, TeamID, TeamRepository as BaseRepository


class TeamRepository(BaseRepository):
    def __init__(self):
        self._team_id_dict = {}
        self._team_name_dict = {}
    
    def AddTeam(self, name, *args, **kwargs):
        if name in self._team_name_dict:
            raise ValueError('Team already exists for name ' + str(name))
            
        ID = TeamID(uuid4())
        value = Team(ID, name, *args, **kwargs)
        
        self._team_id_dict[ID] = value
        self._team_name_dict[name] = value
        
        return value

    def FindTeam(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        return self._team_id_dict.get(ID)
        
    def FindTeamByName(self, name):
        return self._team_name_dict.get(name)
        
    def AllTeams(self):
        return self._team_name_dict.values()
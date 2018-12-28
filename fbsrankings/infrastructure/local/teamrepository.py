from fbsrankings.domain import TeamID, TeamRepository as BaseRepository


class TeamRepository(BaseRepository):
    def __init__(self):
        self._team_id_dict = {}
        self._team_name_dict = {}
    
    def add_team(self, team):
        if team.name in self._team_name_dict:
            raise ValueError('Team already exists for name ' + str(team.name))
            
        self._team_id_dict[team.ID] = team
        self._team_name_dict[team.name] = team

    def find_team(self, ID):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        return self._team_id_dict.get(ID)
        
    def find_team_by_name(self, name):
        return self._team_name_dict.get(name)
        
    def all_teams(self):
        return self._team_name_dict.values()

class TeamDto (object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name


class TeamStorage (object):
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

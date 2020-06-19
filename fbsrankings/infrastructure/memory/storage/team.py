class TeamDto (object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name


class TeamStorage (object):
    def __init__(self):
        self._by_ID = {}
        self._by_key = {}
    
    def add(self, team):
        if not isinstance(team, TeamDto):
            raise TypeError('team must be of type TeamDto')
            
        if team.name in self._by_key:
            raise ValueError(f'Team already exists for name {team.name}')
            
        self._by_ID[team.ID] = team
        self._by_key[team.name] = team

    def get(self, ID):
        return self._by_ID.get(ID)
        
    def find(self, name):
        return self._by_key.get(name)
        
    def all(self):
        return self._by_key.values()

from fbsrankings.common.identifier import Identifier


class TeamID (Identifier):
    pass


class Team (object):
    def __init__(self, ID, name):
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        self.ID = ID
        
        self.name = name


class TeamRepository (object):
    def add_team(self, name, *args, **kwargs):
        pass

    def find_team(self, ID):
        pass
        
    def find_team_by_name(self, name):
        pass
    
    def all_teams(self):
        pass

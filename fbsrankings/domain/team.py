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
    def AddTeam(self, name, *args, **kwargs):
        pass

    def FindTeam(self, ID):
        pass
        
    def FindTeamByName(self, name):
        pass
    
    def AllTeams(self):
        pass
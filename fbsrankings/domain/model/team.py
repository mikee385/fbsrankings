from uuid import uuid4

from fbsrankings.common import Identifier, EventBus
from fbsrankings.event import TeamRegisteredEvent


class TeamID (Identifier):
    pass


class Team (object):
    def __init__(self, event_bus, ID, name):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        self._ID = ID
        
        self._name = name
        
    @property
    def ID(self):
        return self._ID
        
    @property
    def name(self):
        return self._name


class TeamRepository (object):
    @property
    def event_bus(self):
        raise NotImplementedError

    def find_by_ID(self, ID):
        raise NotImplementedError
        
    def find_by_name(self, name):
        raise NotImplementedError
    
    def all(self):
        raise NotImplementedError
        

class TeamManager (TeamRepository):
    def __init__(self, repository):
        if not isinstance(repository, TeamRepository):
            raise TypeError('event_bus must be of type TeamRepository')
        self._repository = repository
        
    @property
    def event_bus(self):
        return self._repository.event_bus
    
    def register(self, name):
        ID = TeamID(uuid4())
        team = Team(self.event_bus, ID, name)
        self.event_bus.raise_event(TeamRegisteredEvent(team.ID, team.name))
        
        return team
        
    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_name(self, name):
        return self._repository.find_by_name(name)
    
    def all(self):
        return self._repository.all()

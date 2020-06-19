from uuid import uuid4

from fbsrankings.common import Identifier, EventBus
from fbsrankings.event import TeamCreatedEvent


class TeamID (Identifier):
    pass


class Team (object):
    def __init__(self, bus, ID, name):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        
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
    def __init__(self, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
    
    def create(self, name):
        ID = TeamID(uuid4())
        team = Team(self._bus, ID, name)
        self._bus.publish(TeamCreatedEvent(team.ID, team.name))
        
        return team

    def get(self, ID):
        raise NotImplementedError
        
    def find(self, name):
        raise NotImplementedError

from uuid import uuid4

from fbsrankings.common import Identifier, Event, EventBus


class TeamID (Identifier):
    pass


class Team (object):
    def __init__(self, event_bus, ID, name):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        if not isinstance(ID, TeamID):
            raise TypeError('ID must be of type TeamID')
        self.ID = ID
        
        self.name = name


class TeamFactory (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._event_bus.register_type(TeamRegisteredEvent)
        
    def new_team(self, name):
        ID = TeamID(uuid4())
        team = Team(self._event_bus, ID, name)
        team._event_bus.raise_event(TeamRegisteredEvent(team.ID, team.name))
        
        return team


class TeamRepository (object):
    def add_team(self, team):
        raise NotImplementedError

    def find_team(self, ID):
        raise NotImplementedError
        
    def find_team_by_name(self, name):
        raise NotImplementedError
    
    def all_teams(self):
        raise NotImplementedError


class TeamRegisteredEvent (Event):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
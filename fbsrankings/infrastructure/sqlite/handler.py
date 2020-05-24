import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.domain import Repository
from fbsrankings.infrastructure.sqlite import SeasonQueryHandler, SeasonEventHandler, TeamQueryHandler, TeamEventHandler, AffiliationQueryHandler, AffiliationEventHandler, GameQueryHandler, GameEventHandler


class QueryHandler (Repository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
            
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        
        super().__init__(
            SeasonQueryHandler(connection, event_bus),
            TeamQueryHandler(connection, event_bus),
            AffiliationQueryHandler(connection, event_bus),
            GameQueryHandler(connection, event_bus)
        )
        

class EventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('connection must be of type sqlite3.Cursor')
            
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        
        self.season = SeasonEventHandler(cursor, event_bus),
        self.team = TeamEventHandler(cursor, event_bus),
        self.affiliation = AffiliationEventHandler(cursor, event_bus),
        self.game = GameEventHandler(cursor, event_bus)

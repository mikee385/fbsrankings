import sqlite3

from fbsrankings.common import QueryBus
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery
from fbsrankings.infrastructure.sqlite.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler


class QueryHandler (object):
    def __init__(self, database, query_bus):
        if not isinstance(query_bus, QueryBus):
            raise TypeError('query_bus must be of type QueryBus')
        self._bus = query_bus
            
        self._connection = sqlite3.connect(database)
        self._connection.execute('PRAGMA query_only = ON')
        
        self._handlers = {}
        
        self._handlers[AffiliationCountBySeasonQuery] = AffiliationCountBySeasonQueryHandler(self._connection)
        self._handlers[CanceledGamesQuery] = CanceledGamesQueryHandler(self._connection)
        self._handlers[GameByIDQuery] = GameByIDQueryHandler(self._connection)
        self._handlers[GameCountBySeasonQuery] = GameCountBySeasonQueryHandler(self._connection)
        self._handlers[SeasonByIDQuery] = SeasonByIDQueryHandler(self._connection)
        self._handlers[SeasonsQuery] = SeasonsQueryHandler(self._connection)
        self._handlers[TeamByIDQuery] = TeamByIDQueryHandler(self._connection)
        self._handlers[TeamCountBySeasonQuery] = TeamCountBySeasonQueryHandler(self._connection)
            
        for query, handler in self._handlers.items():
            self._bus.register_handler(query, handler)
        
    def close(self):
        for query, handler in self._handlers.items():
            self._bus.unregister_handler(query, handler)
            
        self._connection.close()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

from fbsrankings.common import QueryBus
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler


class QueryHandler (object):
    def __init__(self, storage, query_bus):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
            
        if not isinstance(query_bus, QueryBus):
            raise TypeError('query_bus must be of type QueryBus')
        self._bus = query_bus
        
        self._handlers = {}
        
        self._handlers[AffiliationCountBySeasonQuery] = AffiliationCountBySeasonQueryHandler(storage)
        self._handlers[CanceledGamesQuery] = CanceledGamesQueryHandler(storage)
        self._handlers[GameByIDQuery] = GameByIDQueryHandler(storage)
        self._handlers[GameCountBySeasonQuery] = GameCountBySeasonQueryHandler(storage)
        self._handlers[SeasonByIDQuery] = SeasonByIDQueryHandler(storage)
        self._handlers[SeasonsQuery] = SeasonsQueryHandler(storage)
        self._handlers[TeamByIDQuery] = TeamByIDQueryHandler(storage)
        self._handlers[TeamCountBySeasonQuery] = TeamCountBySeasonQueryHandler(storage)
        
        for query, handler in self._handlers.items():
            self._bus.register_handler(query, handler)
        
    def close(self):
        for query, handler in self._handlers.items():
            self._bus.unregister_handler(query, handler)
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

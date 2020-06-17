import sqlite3

from fbsrankings.common import QueryBus
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery
from fbsrankings.infrastructure.sqlite.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler


class QueryHandler (object):
    def __init__(self, database, bus):
        if not isinstance(bus, QueryBus):
            raise TypeError('bus must be of type QueryBus')
            
        self._connection = sqlite3.connect(database)
        self._connection.execute('PRAGMA query_only = ON')
            
        bus.register_handler(AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(self._connection))
        bus.register_handler(CanceledGamesQuery, CanceledGamesQueryHandler(self._connection))
        bus.register_handler(GameByIDQuery, GameByIDQueryHandler(self._connection))
        bus.register_handler(GameCountBySeasonQuery, GameCountBySeasonQueryHandler(self._connection))
        bus.register_handler(SeasonByIDQuery, SeasonByIDQueryHandler(self._connection))
        bus.register_handler(SeasonsQuery, SeasonsQueryHandler(self._connection))
        bus.register_handler(TeamByIDQuery, TeamByIDQueryHandler(self._connection))
        bus.register_handler(TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(self._connection))
        
    def close(self):
        self._connection.close()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

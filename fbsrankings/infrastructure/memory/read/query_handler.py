from fbsrankings.common import QueryBus
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler


class QueryHandler (object):
    def __init__(self, storage, bus):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
            
        if not isinstance(bus, QueryBus):
            raise TypeError('bus must be of type QueryBus')
            
        bus.register_handler(AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(storage))
        bus.register_handler(CanceledGamesQuery, CanceledGamesQueryHandler(storage))
        bus.register_handler(GameByIDQuery, GameByIDQueryHandler(storage))
        bus.register_handler(GameCountBySeasonQuery, GameCountBySeasonQueryHandler(storage))
        bus.register_handler(SeasonByIDQuery, SeasonByIDQueryHandler(storage))
        bus.register_handler(SeasonsQuery, SeasonsQueryHandler(storage))
        bus.register_handler(TeamByIDQuery, TeamByIDQueryHandler(storage))
        bus.register_handler(TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(storage))
        
    def close(self):
        pass
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False

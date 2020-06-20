import sqlite3

from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManager as BaseQueryManager
from fbsrankings.infrastructure.sqlite.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery


class QueryManager (BaseQueryManager):
    def __init__(self, database: str, query_bus: QueryBus) -> None:
        super().__init__(query_bus)
            
        self._connection = sqlite3.connect(database)
        self._connection.execute('PRAGMA query_only = ON')
        
        self.register_hander(AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(self._connection))
        self.register_hander(CanceledGamesQuery, CanceledGamesQueryHandler(self._connection))
        self.register_hander(GameByIDQuery, GameByIDQueryHandler(self._connection))
        self.register_hander(GameCountBySeasonQuery, GameCountBySeasonQueryHandler(self._connection))
        self.register_hander(SeasonByIDQuery, SeasonByIDQueryHandler(self._connection))
        self.register_hander(SeasonsQuery, SeasonsQueryHandler(self._connection))
        self.register_hander(TeamByIDQuery, TeamByIDQueryHandler(self._connection))
        self.register_hander(TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(self._connection))
        
    def close(self) -> None:
        super().close()
        self._connection.close()

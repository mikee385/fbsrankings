from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManager as BaseQueryManager
from fbsrankings.infrastructure.memory.read import AffiliationCountBySeasonQueryHandler, CanceledGamesQueryHandler, GameByIDQueryHandler, GameCountBySeasonQueryHandler, SeasonByIDQueryHandler, SeasonsQueryHandler, TeamByIDQueryHandler, TeamCountBySeasonQueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery


class QueryManager (BaseQueryManager):
    def __init__(self, storage: Storage, query_bus: QueryBus) -> None:
        super().__init__(query_bus)

        self.register_hander(AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(storage))
        self.register_hander(CanceledGamesQuery, CanceledGamesQueryHandler(storage))
        self.register_hander(GameByIDQuery, GameByIDQueryHandler(storage))
        self.register_hander(GameCountBySeasonQuery, GameCountBySeasonQueryHandler(storage))
        self.register_hander(SeasonByIDQuery, SeasonByIDQueryHandler(storage))
        self.register_hander(SeasonsQuery, SeasonsQueryHandler(storage))
        self.register_hander(TeamByIDQuery, TeamByIDQueryHandler(storage))
        self.register_hander(TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(storage))

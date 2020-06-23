from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManager as BaseQueryManager
from fbsrankings.infrastructure.memory.read.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.read.canceled_games import (
    CanceledGamesQueryHandler,
)
from fbsrankings.infrastructure.memory.read.game_by_id import GameByIDQueryHandler
from fbsrankings.infrastructure.memory.read.game_count_by_season import (
    GameCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.read.season_by_id import SeasonByIDQueryHandler
from fbsrankings.infrastructure.memory.read.seasons import SeasonsQueryHandler
from fbsrankings.infrastructure.memory.read.team_by_id import TeamByIDQueryHandler
from fbsrankings.infrastructure.memory.read.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import (
    AffiliationCountBySeasonQuery,
    CanceledGamesQuery,
    GameByIDQuery,
    GameCountBySeasonQuery,
    SeasonByIDQuery,
    SeasonsQuery,
    TeamByIDQuery,
    TeamCountBySeasonQuery,
)


class QueryManager(BaseQueryManager):
    def __init__(self, storage: Storage, query_bus: QueryBus) -> None:
        super().__init__(query_bus)

        self.register_hander(
            AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(storage)
        )
        self.register_hander(CanceledGamesQuery, CanceledGamesQueryHandler(storage))
        self.register_hander(GameByIDQuery, GameByIDQueryHandler(storage))
        self.register_hander(
            GameCountBySeasonQuery, GameCountBySeasonQueryHandler(storage)
        )
        self.register_hander(SeasonByIDQuery, SeasonByIDQueryHandler(storage))
        self.register_hander(SeasonsQuery, SeasonsQueryHandler(storage))
        self.register_hander(TeamByIDQuery, TeamByIDQueryHandler(storage))
        self.register_hander(
            TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(storage)
        )

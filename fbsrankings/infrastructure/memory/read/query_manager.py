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
from fbsrankings.infrastructure.memory.read.game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.memory.read.most_recent_completed_week import (
    MostRecentCompletedWeekQueryHandler,
)
from fbsrankings.infrastructure.memory.read.season_by_id import SeasonByIDQueryHandler
from fbsrankings.infrastructure.memory.read.season_by_year import (
    SeasonByYearQueryHandler,
)
from fbsrankings.infrastructure.memory.read.seasons import SeasonsQueryHandler
from fbsrankings.infrastructure.memory.read.team_by_id import TeamByIDQueryHandler
from fbsrankings.infrastructure.memory.read.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.read.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.memory.read.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.memory.read.week_count_by_season import (
    WeekCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import MostRecentCompletedWeekQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import WeekCountBySeasonQuery


class QueryManager(BaseQueryManager):
    def __init__(self, storage: Storage, query_bus: QueryBus) -> None:
        super().__init__(query_bus)

        self.register_handler(
            AffiliationCountBySeasonQuery, AffiliationCountBySeasonQueryHandler(storage)
        )
        self.register_handler(CanceledGamesQuery, CanceledGamesQueryHandler(storage))
        self.register_handler(GameByIDQuery, GameByIDQueryHandler(storage))
        self.register_handler(
            GameCountBySeasonQuery, GameCountBySeasonQueryHandler(storage)
        )
        self.register_handler(
            GameRankingBySeasonWeekQuery, GameRankingBySeasonWeekQueryHandler(storage)
        )
        self.register_handler(
            MostRecentCompletedWeekQuery, MostRecentCompletedWeekQueryHandler(storage)
        )
        self.register_handler(SeasonByIDQuery, SeasonByIDQueryHandler(storage))
        self.register_handler(SeasonByYearQuery, SeasonByYearQueryHandler(storage))
        self.register_handler(SeasonsQuery, SeasonsQueryHandler(storage))
        self.register_handler(TeamByIDQuery, TeamByIDQueryHandler(storage))
        self.register_handler(
            TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(storage)
        )
        self.register_handler(
            TeamRankingBySeasonWeekQuery, TeamRankingBySeasonWeekQueryHandler(storage)
        )
        self.register_handler(
            TeamRecordBySeasonWeekQuery, TeamRecordBySeasonWeekQueryHandler(storage)
        )
        self.register_handler(
            WeekCountBySeasonQuery, WeekCountBySeasonQueryHandler(storage)
        )

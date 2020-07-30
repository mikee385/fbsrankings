"""Read-model for the in-memory repositories of the fbsrankings package"""
from .affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler as AffiliationCountBySeasonQueryHandler,
)
from .canceled_games import CanceledGamesQueryHandler as CanceledGamesQueryHandler
from .game_by_id import GameByIDQueryHandler as GameByIDQueryHandler
from .game_count_by_season import (
    GameCountBySeasonQueryHandler as GameCountBySeasonQueryHandler,
)
from .game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryHandler as GameRankingBySeasonWeekQueryHandler,
)
from .latest_season_week import (
    LatestSeasonWeekQueryHandler as LatestSeasonWeekQueryHandler,
)
from .query_manager import QueryManager as QueryManager
from .season_by_id import SeasonByIDQueryHandler as SeasonByIDQueryHandler
from .season_by_year import SeasonByYearQueryHandler as SeasonByYearQueryHandler
from .seasons import SeasonsQueryHandler as SeasonsQueryHandler
from .team_by_id import TeamByIDQueryHandler as TeamByIDQueryHandler
from .team_count_by_season import (
    TeamCountBySeasonQueryHandler as TeamCountBySeasonQueryHandler,
)
from .team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler as TeamRankingBySeasonWeekQueryHandler,
)
from .team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler as TeamRecordBySeasonWeekQueryHandler,
)
from .week_count_by_season import (
    WeekCountBySeasonQueryHandler as WeekCountBySeasonQueryHandler,
)

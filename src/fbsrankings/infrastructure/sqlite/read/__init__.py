"""Read-model for the sqlite3 repositories of the fbsrankings package"""
from .affiliation_count_by_season import AffiliationCountBySeasonQueryHandler
from .canceled_games import CanceledGamesQueryHandler
from .game_by_id import GameByIDQueryHandler
from .game_count_by_season import GameCountBySeasonQueryHandler
from .game_ranking_by_season_week import GameRankingBySeasonWeekQueryHandler
from .latest_season_week import LatestSeasonWeekQueryHandler
from .query_manager import QueryManager
from .season_by_id import SeasonByIDQueryHandler
from .season_by_year import SeasonByYearQueryHandler
from .seasons import SeasonsQueryHandler
from .team_by_id import TeamByIDQueryHandler
from .team_count_by_season import TeamCountBySeasonQueryHandler
from .team_ranking_by_season_week import TeamRankingBySeasonWeekQueryHandler
from .team_record_by_season_week import TeamRecordBySeasonWeekQueryHandler
from .week_count_by_season import WeekCountBySeasonQueryHandler

__all__ = [
    "AffiliationCountBySeasonQueryHandler",
    "CanceledGamesQueryHandler",
    "GameByIDQueryHandler",
    "GameCountBySeasonQueryHandler",
    "GameRankingBySeasonWeekQueryHandler",
    "LatestSeasonWeekQueryHandler",
    "QueryManager",
    "SeasonByIDQueryHandler",
    "SeasonByYearQueryHandler",
    "SeasonsQueryHandler",
    "TeamByIDQueryHandler",
    "TeamCountBySeasonQueryHandler",
    "TeamRankingBySeasonWeekQueryHandler",
    "TeamRecordBySeasonWeekQueryHandler",
    "WeekCountBySeasonQueryHandler",
]

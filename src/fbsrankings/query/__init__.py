"""Query classes for the fbsrankings package"""
from .affiliation_count_by_season import AffiliationCountBySeasonQuery
from .affiliation_count_by_season import AffiliationCountBySeasonResult
from .canceled_games import CanceledGameResult
from .canceled_games import CanceledGamesQuery
from .canceled_games import CanceledGamesResult
from .game_by_id import GameByIDQuery
from .game_by_id import GameByIDResult
from .game_count_by_season import GameCountBySeasonQuery
from .game_count_by_season import GameCountBySeasonResult
from .game_ranking_by_season_week import GameRankingBySeasonWeekQuery
from .game_ranking_by_season_week import GameRankingBySeasonWeekResult
from .game_ranking_by_season_week import GameRankingValueBySeasonWeekResult
from .latest_season_week import LatestSeasonWeekQuery
from .latest_season_week import LatestSeasonWeekResult
from .postseason_game_count_by_season import PostseasonGameCountBySeasonQuery
from .postseason_game_count_by_season import PostseasonGameCountBySeasonResult
from .season_by_id import SeasonByIDQuery
from .season_by_id import SeasonByIDResult
from .season_by_year import SeasonByYearQuery
from .season_by_year import SeasonByYearResult
from .seasons import SeasonResult
from .seasons import SeasonsQuery
from .seasons import SeasonsResult
from .team_by_id import TeamByIDQuery
from .team_by_id import TeamByIDResult
from .team_count_by_season import TeamCountBySeasonQuery
from .team_count_by_season import TeamCountBySeasonResult
from .team_ranking_by_season_week import TeamRankingBySeasonWeekQuery
from .team_ranking_by_season_week import TeamRankingBySeasonWeekResult
from .team_ranking_by_season_week import TeamRankingValueBySeasonWeekResult
from .team_record_by_season_week import TeamRecordBySeasonWeekQuery
from .team_record_by_season_week import TeamRecordBySeasonWeekResult
from .team_record_by_season_week import TeamRecordValueBySeasonWeekResult
from .week_count_by_season import WeekCountBySeasonQuery
from .week_count_by_season import WeekCountBySeasonResult

__all__ = [
    "AffiliationCountBySeasonQuery",
    "AffiliationCountBySeasonResult",
    "CanceledGameResult",
    "CanceledGamesQuery",
    "CanceledGamesResult",
    "GameByIDQuery",
    "GameByIDResult",
    "GameCountBySeasonQuery",
    "GameCountBySeasonResult",
    "GameRankingBySeasonWeekQuery",
    "GameRankingBySeasonWeekResult",
    "GameRankingValueBySeasonWeekResult",
    "LatestSeasonWeekQuery",
    "LatestSeasonWeekResult",
    "PostseasonGameCountBySeasonQuery",
    "PostseasonGameCountBySeasonResult",
    "SeasonByIDQuery",
    "SeasonByIDResult",
    "SeasonByYearQuery",
    "SeasonByYearResult",
    "SeasonResult",
    "SeasonsQuery",
    "SeasonsResult",
    "TeamByIDQuery",
    "TeamByIDResult",
    "TeamCountBySeasonQuery",
    "TeamCountBySeasonResult",
    "TeamRankingBySeasonWeekQuery",
    "TeamRankingBySeasonWeekResult",
    "TeamRankingValueBySeasonWeekResult",
    "TeamRecordBySeasonWeekQuery",
    "TeamRecordBySeasonWeekResult",
    "TeamRecordValueBySeasonWeekResult",
    "WeekCountBySeasonQuery",
    "WeekCountBySeasonResult",
]

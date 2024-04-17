"""Query classes for the core module of the fbsrankings package"""

from .query.affiliation_count_by_season import AffiliationCountBySeasonQuery
from .query.affiliation_count_by_season import AffiliationCountBySeasonResult
from .query.affiliations_by_season import AffiliationBySeasonResult
from .query.affiliations_by_season import AffiliationsBySeasonQuery
from .query.affiliations_by_season import AffiliationsBySeasonResult
from .query.canceled_games import CanceledGameResult
from .query.canceled_games import CanceledGamesQuery
from .query.canceled_games import CanceledGamesResult
from .query.game_by_id import GameByIDQuery
from .query.game_by_id import GameByIDResult
from .query.game_count_by_season import GameCountBySeasonQuery
from .query.game_count_by_season import GameCountBySeasonResult
from .query.games_by_season import GameBySeasonResult
from .query.games_by_season import GamesBySeasonQuery
from .query.games_by_season import GamesBySeasonResult
from .query.latest_season_week import LatestSeasonWeekQuery
from .query.latest_season_week import LatestSeasonWeekResult
from .query.postseason_game_count_by_season import PostseasonGameCountBySeasonQuery
from .query.postseason_game_count_by_season import PostseasonGameCountBySeasonResult
from .query.season_by_id import SeasonByIDQuery
from .query.season_by_id import SeasonByIDResult
from .query.season_by_year import SeasonByYearQuery
from .query.season_by_year import SeasonByYearResult
from .query.seasons import SeasonResult
from .query.seasons import SeasonsQuery
from .query.seasons import SeasonsResult
from .query.team_by_id import TeamByIDQuery
from .query.team_by_id import TeamByIDResult
from .query.team_count_by_season import TeamCountBySeasonQuery
from .query.team_count_by_season import TeamCountBySeasonResult
from .query.teams import TeamResult
from .query.teams import TeamsQuery
from .query.teams import TeamsResult
from .query.week_count_by_season import WeekCountBySeasonQuery
from .query.week_count_by_season import WeekCountBySeasonResult
from .query_bus import QueryBus


__all__ = [
    "AffiliationBySeasonResult",
    "AffiliationCountBySeasonQuery",
    "AffiliationCountBySeasonResult",
    "AffiliationsBySeasonQuery",
    "AffiliationsBySeasonResult",
    "CanceledGameResult",
    "CanceledGamesQuery",
    "CanceledGamesResult",
    "GameByIDQuery",
    "GameByIDResult",
    "GameBySeasonResult",
    "GameCountBySeasonQuery",
    "GameCountBySeasonResult",
    "GamesBySeasonQuery",
    "GamesBySeasonResult",
    "LatestSeasonWeekQuery",
    "LatestSeasonWeekResult",
    "PostseasonGameCountBySeasonQuery",
    "PostseasonGameCountBySeasonResult",
    "QueryBus",
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
    "TeamResult",
    "TeamsQuery",
    "TeamsResult",
    "WeekCountBySeasonQuery",
    "WeekCountBySeasonResult",
]

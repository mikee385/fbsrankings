"""Query message classes for the fbsrankings package"""

from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from communication.bus import Query

from .affiliation_count_by_season import AffiliationCountBySeasonQuery
from .affiliation_count_by_season import AffiliationCountBySeasonResult
from .affiliations_by_season import AffiliationBySeasonResult
from .affiliations_by_season import AffiliationsBySeasonQuery
from .affiliations_by_season import AffiliationsBySeasonResult
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
from .games_by_season import GameBySeasonResult
from .games_by_season import GamesBySeasonQuery
from .games_by_season import GamesBySeasonResult
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
from .teams import TeamResult
from .teams import TeamsQuery
from .teams import TeamsResult
from .week_count_by_season import WeekCountBySeasonQuery
from .week_count_by_season import WeekCountBySeasonResult


R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


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
    "GameRankingBySeasonWeekQuery",
    "GameRankingBySeasonWeekResult",
    "GameRankingValueBySeasonWeekResult",
    "GamesBySeasonQuery",
    "GamesBySeasonResult",
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
    "TeamResult",
    "TeamsQuery",
    "TeamsResult",
    "WeekCountBySeasonQuery",
    "WeekCountBySeasonResult",
]

ResultTypes: Dict[Type[Query[Any]], Type[Any]] = {
    AffiliationCountBySeasonQuery: AffiliationCountBySeasonResult,
    AffiliationsBySeasonQuery: AffiliationsBySeasonResult,
    CanceledGamesQuery: CanceledGamesResult,
    GameByIDQuery: GameByIDResult,
    GameCountBySeasonQuery: GameCountBySeasonResult,
    GameRankingBySeasonWeekQuery: GameRankingBySeasonWeekResult,
    GamesBySeasonQuery: GamesBySeasonResult,
    LatestSeasonWeekQuery: LatestSeasonWeekResult,
    PostseasonGameCountBySeasonQuery: PostseasonGameCountBySeasonResult,
    SeasonByIDQuery: SeasonByIDResult,
    SeasonByYearQuery: SeasonByYearResult,
    SeasonsQuery: SeasonsResult,
    TeamByIDQuery: TeamByIDResult,
    TeamCountBySeasonQuery: TeamCountBySeasonResult,
    TeamRankingBySeasonWeekQuery: TeamRankingBySeasonWeekResult,
    TeamRecordBySeasonWeekQuery: TeamRecordBySeasonWeekResult,
    TeamsQuery: TeamsResult,
    WeekCountBySeasonQuery: WeekCountBySeasonResult,
}

Topics: Dict[Type[Query[Any]], str] = {
    AffiliationCountBySeasonQuery: "fbsrankings/query/affiliation_count_by_season",
    AffiliationsBySeasonQuery: "fbsrankings/query/affiliations_by_season",
    CanceledGamesQuery: "fbsrankings/query/canceled_games",
    GameByIDQuery: "fbsrankings/query/game_by_id",
    GameCountBySeasonQuery: "fbsrankings/query/game_count_by_season",
    GameRankingBySeasonWeekQuery: "fbsrankings/query/game_ranking_by_season_week",
    GamesBySeasonQuery: "fbsrankings/query/games_by_season",
    LatestSeasonWeekQuery: "fbsrankings/query/latest_season_week",
    PostseasonGameCountBySeasonQuery: "fbsrankings/query/postseason_game_count_by_season",
    SeasonByIDQuery: "fbsrankings/query/season_by_id",
    SeasonByYearQuery: "fbsrankings/query/season_by_year",
    SeasonsQuery: "fbsrankings/query/seasons",
    TeamByIDQuery: "fbsrankings/query/team_by_id",
    TeamCountBySeasonQuery: "fbsrankings/query/team_count_by_season",
    TeamRankingBySeasonWeekQuery: "fbsrankings/query/team_ranking_by_season_week",
    TeamRecordBySeasonWeekQuery: "fbsrankings/query/team_record_by_season_week",
    TeamsQuery: "fbsrankings/query/teams",
    WeekCountBySeasonQuery: "fbsrankings/query/week_count_by_season",
}

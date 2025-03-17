"""Query message classes for the fbsrankings package"""

from typing import Any

from communication.messages import Query

from .affiliation_count_by_season_pb2 import AffiliationCountBySeasonQuery
from .affiliation_count_by_season_pb2 import AffiliationCountBySeasonResult
from .affiliations_by_season_pb2 import AffiliationBySeasonResult
from .affiliations_by_season_pb2 import AffiliationsBySeasonQuery
from .affiliations_by_season_pb2 import AffiliationsBySeasonResult
from .canceled_games_pb2 import CanceledGameResult
from .canceled_games_pb2 import CanceledGamesQuery
from .canceled_games_pb2 import CanceledGamesResult
from .game_by_id_pb2 import GameByIDQuery
from .game_by_id_pb2 import GameByIDResult
from .game_count_by_season_pb2 import GameCountBySeasonQuery
from .game_count_by_season_pb2 import GameCountBySeasonResult
from .game_ranking_by_season_week_pb2 import GameRankingBySeasonWeekQuery
from .game_ranking_by_season_week_pb2 import GameRankingBySeasonWeekResult
from .game_ranking_by_season_week_pb2 import GameRankingValueBySeasonWeekResult
from .games_by_season_pb2 import GameBySeasonResult
from .games_by_season_pb2 import GamesBySeasonQuery
from .games_by_season_pb2 import GamesBySeasonResult
from .latest_season_week_pb2 import LatestSeasonWeekQuery
from .latest_season_week_pb2 import LatestSeasonWeekResult
from .postseason_game_count_by_season_pb2 import PostseasonGameCountBySeasonQuery
from .postseason_game_count_by_season_pb2 import PostseasonGameCountBySeasonResult
from .season_by_id_pb2 import SeasonByIDQuery
from .season_by_id_pb2 import SeasonByIDResult
from .season_by_year_pb2 import SeasonByYearQuery
from .season_by_year_pb2 import SeasonByYearResult
from .seasons_pb2 import SeasonResult
from .seasons_pb2 import SeasonsQuery
from .seasons_pb2 import SeasonsResult
from .team_by_id_pb2 import TeamByIDQuery
from .team_by_id_pb2 import TeamByIDResult
from .team_count_by_season_pb2 import TeamCountBySeasonQuery
from .team_count_by_season_pb2 import TeamCountBySeasonResult
from .team_ranking_by_season_week_pb2 import TeamRankingBySeasonWeekQuery
from .team_ranking_by_season_week_pb2 import TeamRankingBySeasonWeekResult
from .team_ranking_by_season_week_pb2 import TeamRankingValueBySeasonWeekResult
from .team_record_by_season_week_pb2 import TeamRecordBySeasonWeekQuery
from .team_record_by_season_week_pb2 import TeamRecordBySeasonWeekResult
from .team_record_by_season_week_pb2 import TeamRecordValueBySeasonWeekResult
from .teams_pb2 import TeamResult
from .teams_pb2 import TeamsQuery
from .teams_pb2 import TeamsResult
from .week_count_by_season_pb2 import WeekCountBySeasonQuery
from .week_count_by_season_pb2 import WeekCountBySeasonResult


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

Topics: dict[type[Query[Any]], str] = {
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

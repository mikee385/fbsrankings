import datetime
from typing import List
from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class GameRankingValueBySeasonWeekResult:
    game_id: str
    season_id: str
    year: int
    week: int
    date: datetime.date
    season_section: str
    home_team_id: str
    home_team_name: str
    away_team_id: str
    away_team_name: str
    home_team_score: Optional[int]
    away_team_score: Optional[int]
    status: str
    notes: str
    order: int
    rank: int
    value: float


@dataclass(frozen=True)
class GameRankingBySeasonWeekResult:
    ranking_id: str
    name: str
    season_id: str
    year: int
    week: Optional[int]
    values: List[GameRankingValueBySeasonWeekResult]


@dataclass(frozen=True)
class GameRankingBySeasonWeekQuery(Query[Optional[GameRankingBySeasonWeekResult]]):
    query_id: str
    name: str
    season_id: str
    week: Optional[int]

import datetime
from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class GameRankingValueBySeasonWeekResult:
    game_id: UUID
    season_id: UUID
    year: int
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    home_team_name: str
    away_team_id: UUID
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
    ranking_id: UUID  # noqa: F841
    name: str
    season_id: UUID
    year: int
    week: Optional[int]
    values: List[GameRankingValueBySeasonWeekResult]


@dataclass(frozen=True)
class GameRankingBySeasonWeekQuery(Query[Optional[GameRankingBySeasonWeekResult]]):
    query_id: UUID
    name: str
    season_id: UUID
    week: Optional[int]

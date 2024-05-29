import datetime
from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class GameRankingValueBySeasonWeekResult:
    id_: UUID
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
    id_: UUID
    name: str
    season_id: UUID
    year: int
    week: Optional[int]
    values: List[GameRankingValueBySeasonWeekResult]


@dataclass(frozen=True)
class GameRankingBySeasonWeekQuery(Query[Optional[GameRankingBySeasonWeekResult]]):
    name: str
    season_id: UUID
    week: Optional[int]

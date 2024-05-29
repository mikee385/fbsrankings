from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class TeamRankingValueBySeasonWeekResult:
    id_: UUID
    name: str
    order: int
    rank: int
    value: float


@dataclass(frozen=True)
class TeamRankingBySeasonWeekResult:
    id_: UUID
    name: str
    season_id: UUID
    year: int
    week: Optional[int]
    values: List[TeamRankingValueBySeasonWeekResult]


@dataclass(frozen=True)
class TeamRankingBySeasonWeekQuery(Query[Optional[TeamRankingBySeasonWeekResult]]):
    name: str
    season_id: UUID
    week: Optional[int]

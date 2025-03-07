from typing import List
from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamRankingValueBySeasonWeekResult:
    team_id: str
    name: str
    order: int
    rank: int
    value: float


@dataclass(frozen=True)
class TeamRankingBySeasonWeekResult:
    ranking_id: str
    name: str
    season_id: str
    year: int
    week: Optional[int]
    values: List[TeamRankingValueBySeasonWeekResult]


@dataclass(frozen=True)
class TeamRankingBySeasonWeekQuery(Query[Optional[TeamRankingBySeasonWeekResult]]):
    query_id: str
    name: str
    season_id: str
    week: Optional[int]

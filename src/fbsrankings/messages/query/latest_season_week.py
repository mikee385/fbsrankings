from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class LatestSeasonWeekResult:
    season_id: str
    year: int
    week: Optional[int]


@dataclass(frozen=True)
class LatestSeasonWeekQuery(Query[Optional[LatestSeasonWeekResult]]):
    query_id: str

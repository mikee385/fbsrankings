from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class LatestSeasonWeekResult:
    def __init__(self, season_id: UUID, year: int, week: Optional[int]) -> None:
        self.season_id = season_id
        self.year = year
        self.week = week


class LatestSeasonWeekQuery(Query[Optional[LatestSeasonWeekResult]]):
    pass

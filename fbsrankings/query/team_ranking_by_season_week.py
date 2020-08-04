from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamRankingValueBySeasonWeekResult:
    def __init__(
        self, id: UUID, name: str, order: int, rank: int, value: float,
    ) -> None:
        self.id = id
        self.name = name
        self.order = order
        self.rank = rank
        self.value = value


class TeamRankingBySeasonWeekResult:
    def __init__(
        self,
        id: UUID,
        name: str,
        season_id: UUID,
        year: int,
        week: Optional[int],
        values: List[TeamRankingValueBySeasonWeekResult],
    ) -> None:
        self.id = id
        self.name = name
        self.season_id = season_id
        self.year = year
        self.week = week
        self.values = values


class TeamRankingBySeasonWeekQuery(Query[Optional[TeamRankingBySeasonWeekResult]]):
    def __init__(self, name: str, season_id: UUID, week: Optional[int]) -> None:
        self.name = name
        self.season_id = season_id
        self.week = week

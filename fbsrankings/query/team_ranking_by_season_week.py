from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamRankingValueBySeasonWeekResult(object):
    def __init__(
        self, ID: UUID, name: str, order: int, rank: int, value: float
    ) -> None:
        self.ID = ID
        self.name = name
        self.order = order
        self.rank = rank
        self.value = value


class TeamRankingBySeasonWeekResult(object):
    def __init__(
        self,
        ID: UUID,
        name: str,
        season_ID: UUID,
        year: int,
        week: Optional[int],
        values: List[TeamRankingValueBySeasonWeekResult],
    ) -> None:
        self.ID = ID
        self.name = name
        self.season_ID = season_ID
        self.year = year
        self.week = week
        self.values = values


class TeamRankingBySeasonWeekQuery(Query[Optional[TeamRankingBySeasonWeekResult]]):
    def __init__(self, name: str, season_ID: UUID, week: Optional[int]) -> None:
        self.name = name
        self.season_ID = season_ID
        self.week = week

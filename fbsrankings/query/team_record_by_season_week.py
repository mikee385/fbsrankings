from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamRecordValueBySeasonWeekResult(object):
    def __init__(self, id: UUID, name: str, wins: int, losses: int) -> None:
        self.id = id
        self.name = name
        self.wins = wins
        self.losses = losses

    @property
    def games(self) -> int:
        return self.wins + self.losses

    @property
    def win_percentage(self) -> float:
        return float(self.wins) / self.games if self.wins > 0 else 0.0


class TeamRecordBySeasonWeekResult(object):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        year: int,
        week: Optional[int],
        values: List[TeamRecordValueBySeasonWeekResult],
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.year = year
        self.week = week
        self.values = values


class TeamRecordBySeasonWeekQuery(Query[Optional[TeamRecordBySeasonWeekResult]]):
    def __init__(self, season_id: UUID, week: Optional[int]) -> None:
        self.season_id = season_id
        self.week = week

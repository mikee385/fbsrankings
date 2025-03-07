from typing import List
from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamRecordValueBySeasonWeekResult:
    team_id: str
    name: str
    wins: int
    losses: int


@dataclass(frozen=True)
class TeamRecordBySeasonWeekResult:
    record_id: str
    season_id: str
    year: int
    week: Optional[int]
    values: List[TeamRecordValueBySeasonWeekResult]


@dataclass(frozen=True)
class TeamRecordBySeasonWeekQuery(Query[Optional[TeamRecordBySeasonWeekResult]]):
    query_id: str
    season_id: str
    week: Optional[int]

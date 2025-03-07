from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamRecordValueBySeasonWeekResult:
    team_id: UUID
    name: str
    wins: int
    losses: int


@dataclass(frozen=True)
class TeamRecordBySeasonWeekResult:
    record_id: UUID
    season_id: UUID
    year: int
    week: Optional[int]
    values: List[TeamRecordValueBySeasonWeekResult]


@dataclass(frozen=True)
class TeamRecordBySeasonWeekQuery(Query[Optional[TeamRecordBySeasonWeekResult]]):
    query_id: UUID
    season_id: UUID
    week: Optional[int]

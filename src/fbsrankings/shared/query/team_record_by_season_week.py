from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class TeamRecordValueBySeasonWeekResult:
    id_: UUID
    name: str
    wins: int
    losses: int


@dataclass(frozen=True)
class TeamRecordBySeasonWeekResult:
    id_: UUID
    season_id: UUID
    year: int
    week: Optional[int]
    values: List[TeamRecordValueBySeasonWeekResult]


@dataclass(frozen=True)
class TeamRecordBySeasonWeekQuery(Query[Optional[TeamRecordBySeasonWeekResult]]):
    season_id: UUID
    week: Optional[int]

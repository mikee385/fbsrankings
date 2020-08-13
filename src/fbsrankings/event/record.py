from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class TeamRecordValue:
    team_id: UUID
    wins: int
    losses: int
    games: int
    win_percentage: float


@dataclass(frozen=True)
class TeamRecordCalculatedEvent(Event):
    id_: UUID
    season_id: UUID
    week: Optional[int]
    values: List[TeamRecordValue]

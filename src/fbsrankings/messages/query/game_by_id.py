import datetime
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class GameByIDResult:
    game_id: UUID
    season_id: UUID
    year: int
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    home_team_name: str
    away_team_id: UUID
    away_team_name: str
    home_team_score: Optional[int]
    away_team_score: Optional[int]
    status: str
    notes: str


@dataclass(frozen=True)
class GameByIDQuery(Query[Optional[GameByIDResult]]):
    query_id: UUID
    game_id: UUID

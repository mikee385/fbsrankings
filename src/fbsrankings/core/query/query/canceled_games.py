import datetime
from typing import List
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Query


@dataclass(frozen=True)
class CanceledGameResult:
    id_: UUID
    season_id: UUID
    year: int
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    home_team_name: str
    away_team_id: UUID
    away_team_name: str
    notes: str


@dataclass(frozen=True)
class CanceledGamesResult:
    games: List[CanceledGameResult]


@dataclass(frozen=True)
class CanceledGamesQuery(Query[CanceledGamesResult]):
    pass

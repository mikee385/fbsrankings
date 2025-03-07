import datetime
from typing import List

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class CanceledGameResult:
    game_id: str
    season_id: str
    year: int
    week: int
    date: datetime.date
    season_section: str
    home_team_id: str
    home_team_name: str
    away_team_id: str
    away_team_name: str
    notes: str


@dataclass(frozen=True)
class CanceledGamesResult:
    games: List[CanceledGameResult]


@dataclass(frozen=True)
class CanceledGamesQuery(Query[CanceledGamesResult]):
    query_id: str

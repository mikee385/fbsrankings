import datetime
from typing import List
from uuid import UUID

from fbsrankings.common import Query


class CanceledGameResult:
    def __init__(
        self,
        id_: UUID,
        season_id: UUID,
        year: int,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        home_team_name: str,
        away_team_id: UUID,
        away_team_name: str,
        notes: str,
    ) -> None:
        self.id_ = id_
        self.season_id = season_id
        self.year = year
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.home_team_name = home_team_name
        self.away_team_id = away_team_id
        self.away_team_name = away_team_name
        self.notes = notes


class CanceledGamesResult:
    def __init__(self, games: List[CanceledGameResult]) -> None:
        self.games = games


class CanceledGamesQuery(Query[CanceledGamesResult]):
    pass
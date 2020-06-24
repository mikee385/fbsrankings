import datetime
from typing import List
from uuid import UUID

from fbsrankings.common import Query


class CanceledGameResult(object):
    def __init__(
        self,
        ID: UUID,
        season_ID: UUID,
        year: int,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_ID: UUID,
        home_team_name: str,
        away_team_ID: UUID,
        away_team_name: str,
        notes: str,
    ) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.year = year
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.home_team_name = home_team_name
        self.away_team_ID = away_team_ID
        self.away_team_name = away_team_name
        self.notes = notes


class CanceledGamesResult(object):
    def __init__(self, games: List[CanceledGameResult]) -> None:
        self.games = games


class CanceledGamesQuery(Query[CanceledGamesResult]):
    pass

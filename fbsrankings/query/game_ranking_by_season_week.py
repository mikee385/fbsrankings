import datetime
from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class GameRankingValueBySeasonWeekResult(object):
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
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: str,
        notes: str,
        order: int,
        rank: int,
        value: float,
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
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.status = status
        self.notes = notes
        self.order = order
        self.rank = rank
        self.value = value


class GameRankingBySeasonWeekResult(object):
    def __init__(
        self,
        ID: UUID,
        name: str,
        season_ID: UUID,
        year: int,
        week: Optional[int],
        values: List[GameRankingValueBySeasonWeekResult],
    ) -> None:
        self.ID = ID
        self.name = name
        self.season_ID = season_ID
        self.year = year
        self.week = week
        self.values = values


class GameRankingBySeasonWeekQuery(Query[Optional[GameRankingBySeasonWeekResult]]):
    def __init__(self, name: str, season_ID: UUID, week: Optional[int]) -> None:
        self.name = name
        self.season_ID = season_ID
        self.week = week

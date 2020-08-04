import datetime
from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class GameRankingValueBySeasonWeekResult:
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
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: str,
        notes: str,
        order: int,
        rank: int,
        value: float,
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
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.status = status
        self.notes = notes
        self.order = order
        self.rank = rank
        self.value = value


class GameRankingBySeasonWeekResult:
    def __init__(
        self,
        id_: UUID,
        name: str,
        season_id: UUID,
        year: int,
        week: Optional[int],
        values: List[GameRankingValueBySeasonWeekResult],
    ) -> None:
        self.id_ = id_
        self.name = name
        self.season_id = season_id
        self.year = year
        self.week = week
        self.values = values


class GameRankingBySeasonWeekQuery(Query[Optional[GameRankingBySeasonWeekResult]]):
    def __init__(self, name: str, season_id: UUID, week: Optional[int]) -> None:
        self.name = name
        self.season_id = season_id
        self.week = week

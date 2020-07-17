from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event


class TeamRecordValue(object):
    def __init__(
        self, team_ID: UUID, wins: int, losses: int, games: int, win_percentage: float
    ) -> None:
        self.team_ID = team_ID
        self.wins = wins
        self.losses = losses
        self.games = games
        self.win_percentage = win_percentage


class TeamRecordCalculatedEvent(Event):
    def __init__(
        self,
        ID: UUID,
        season_ID: UUID,
        week: Optional[int],
        values: List[TeamRecordValue],
    ) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.values = values

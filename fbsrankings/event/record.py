from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event


class TeamRecordValue:
    def __init__(
        self, team_id: UUID, wins: int, losses: int, games: int, win_percentage: float,
    ) -> None:
        self.team_id = team_id
        self.wins = wins
        self.losses = losses
        self.games = games
        self.win_percentage = win_percentage


class TeamRecordCalculatedEvent(Event):
    def __init__(
        self,
        id_: UUID,
        season_id: UUID,
        week: Optional[int],
        values: List[TeamRecordValue],
    ) -> None:
        self.id_ = id_
        self.season_id = season_id
        self.week = week
        self.values = values

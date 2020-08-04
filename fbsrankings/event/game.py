import datetime
from uuid import UUID

from fbsrankings.common import Event


class GameCreatedEvent(Event):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        notes: str,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.notes = notes


class GameRescheduledEvent(Event):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        old_week: int,
        old_date: datetime.date,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        notes: str,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.old_week = old_week
        self.old_date = old_date
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.notes = notes


class GameCanceledEvent(Event):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        notes: str,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.notes = notes


class GameCompletedEvent(Event):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        home_team_score: int,
        away_team_score: int,
        notes: str,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.notes = notes


class GameNotesUpdatedEvent(Event):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        old_notes: str,
        notes: str,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.old_notes = old_notes
        self.notes = notes

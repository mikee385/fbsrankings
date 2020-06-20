import datetime

from uuid import UUID

from fbsrankings.common import Event


class GameCreatedEvent (Event):
    def __init__(self, ID: UUID, season_ID: UUID, week: int, date: datetime.date, season_section: str, home_team_ID: UUID, away_team_ID: UUID, notes: str) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
        self.notes = notes
    

class GameRescheduledEvent (Event):
    def __init__(self, ID: UUID, old_week: int, old_date: datetime.date, week: int, date: datetime.date) -> None:
        self.ID = ID
        self.old_week = old_week
        self.old_date = old_date
        self.week = week
        self.date = date
    

class GameCanceledEvent (Event):
    def __init__(self, ID: UUID) -> None:
        self.ID = ID
    

class GameCompletedEvent (Event):
    def __init__(self, ID: UUID, home_team_score: int, away_team_score: int) -> None:
        self.ID = ID
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        

class GameNotesUpdatedEvent (Event):
    def __init__(self, ID: UUID, old_notes: str, notes: str) -> None:
        self.ID = ID
        self.old_notes = old_notes
        self.notes = notes

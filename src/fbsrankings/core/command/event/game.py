import datetime
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class GameCreatedEvent(Event):
    id_: UUID
    season_id: UUID
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    away_team_id: UUID
    notes: str


@dataclass(frozen=True)
class GameRescheduledEvent(Event):
    id_: UUID
    season_id: UUID
    old_week: int
    old_date: datetime.date
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    away_team_id: UUID
    notes: str


@dataclass(frozen=True)
class GameCanceledEvent(Event):
    id_: UUID
    season_id: UUID
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    away_team_id: UUID
    notes: str


@dataclass(frozen=True)
class GameCompletedEvent(Event):
    id_: UUID
    season_id: UUID
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    away_team_id: UUID
    home_team_score: int
    away_team_score: int
    notes: str


@dataclass(frozen=True)
class GameNotesUpdatedEvent(Event):
    id_: UUID
    season_id: UUID
    week: int
    date: datetime.date
    season_section: str
    home_team_id: UUID
    away_team_id: UUID
    old_notes: str
    notes: str

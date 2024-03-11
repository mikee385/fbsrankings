"""Write-model for the in-memory repositories of the fbsrankings package"""
from .affiliation import AffiliationEventHandler
from .affiliation import AffiliationRepository
from .event_handler import EventHandler
from .game import GameEventHandler
from .game import GameRepository
from .ranking import GameRankingEventHandler
from .ranking import GameRankingRepository
from .ranking import TeamRankingEventHandler
from .ranking import TeamRankingRepository
from .record import TeamRecordEventHandler
from .record import TeamRecordRepository
from .repository import Repository
from .season import SeasonEventHandler
from .season import SeasonRepository
from .team import TeamEventHandler
from .team import TeamRepository

__all__ = [
    "AffiliationEventHandler",
    "AffiliationRepository",
    "EventHandler",
    "GameEventHandler",
    "GameRankingEventHandler",
    "GameRankingRepository",
    "GameRepository",
    "Repository",
    "SeasonEventHandler",
    "SeasonRepository",
    "TeamEventHandler",
    "TeamRankingEventHandler",
    "TeamRankingRepository",
    "TeamRecordEventHandler",
    "TeamRecordRepository",
    "TeamRepository",
]

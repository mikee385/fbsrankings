"""Write-model for the in-memory repositories of the fbsrankings package"""
from .affiliation import AffiliationRepository
from .game import GameRepository
from .ranking import GameRankingRepository
from .ranking import TeamRankingRepository
from .record import TeamRecordRepository
from .season import SeasonRepository
from .team import TeamRepository
from .transaction import Transaction

__all__ = [
    "AffiliationRepository",
    "GameRankingRepository",
    "GameRepository",
    "SeasonRepository",
    "TeamRankingRepository",
    "TeamRecordRepository",
    "TeamRepository",
    "Transaction",
]

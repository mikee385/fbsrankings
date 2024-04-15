"""Sqlite storage classes for the fbsrankings package"""
from .affiliation import AffiliationTable
from .game import GameTable
from .ranking import GameRankingValueTable
from .ranking import RankingTable
from .ranking import RankingType
from .ranking import TeamRankingValueTable
from .record import TeamRecordTable
from .record import TeamRecordValueTable
from .season import SeasonTable
from .storage import Storage
from .team import TeamTable


__all__ = [
    "AffiliationTable",
    "GameRankingValueTable",
    "GameTable",
    "RankingTable",
    "RankingType",
    "SeasonTable",
    "Storage",
    "TeamRankingValueTable",
    "TeamRecordTable",
    "TeamRecordValueTable",
    "TeamTable",
]

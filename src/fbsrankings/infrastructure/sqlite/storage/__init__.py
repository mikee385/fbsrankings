"""Storage classes for the sqlite3 repositories of the fbsrankings package"""
from .affiliation import AffiliationTable
from .affiliation import SubdivisionTable
from .game import GameStatusTable
from .game import GameTable
from .ranking import GameRankingValueTable
from .ranking import RankingTable
from .ranking import RankingType
from .ranking import RankingTypeTable
from .ranking import TeamRankingValueTable
from .record import TeamRecordTable
from .record import TeamRecordValueTable
from .season import SeasonSectionTable
from .season import SeasonTable
from .storage import Storage
from .team import TeamTable

__all__ = [
    "AffiliationTable",
    "GameRankingValueTable",
    "GameStatusTable",
    "GameTable",
    "RankingTable",
    "RankingType",
    "RankingTypeTable",
    "SeasonSectionTable",
    "SeasonTable",
    "Storage",
    "SubdivisionTable",
    "TeamRankingValueTable",
    "TeamRecordTable",
    "TeamRecordValueTable",
    "TeamTable",
]

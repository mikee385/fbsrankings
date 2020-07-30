"""Storage classes for the sqlite3 repositories of the fbsrankings package"""
from .affiliation import AffiliationTable as AffiliationTable
from .affiliation import SubdivisionTable as SubdivisionTable
from .game import GameStatusTable as GameStatusTable
from .game import GameTable as GameTable
from .ranking import GameRankingValueTable as GameRankingValueTable
from .ranking import RankingTable as RankingTable
from .ranking import RankingType as RankingType
from .ranking import RankingTypeTable as RankingTypeTable
from .ranking import TeamRankingValueTable as TeamRankingValueTable
from .record import TeamRecordTable as TeamRecordTable
from .record import TeamRecordValueTable as TeamRecordValueTable
from .season import SeasonSectionTable as SeasonSectionTable
from .season import SeasonTable as SeasonTable
from .storage import Storage as Storage
from .team import TeamTable as TeamTable

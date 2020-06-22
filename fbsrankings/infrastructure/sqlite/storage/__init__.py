"""Storage classes for the sqlite3 repositories of the fbsrankings package"""

from fbsrankings.infrastructure.sqlite.storage.affiliation import SubdivisionTable as SubdivisionTable, AffiliationTable as AffiliationTable
from fbsrankings.infrastructure.sqlite.storage.game import GameStatusTable as GameStatusTable, GameTable as GameTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonSectionTable as SeasonSectionTable, SeasonTable as SeasonTable
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable as TeamTable
from fbsrankings.infrastructure.sqlite.storage.storage import Storage as Storage

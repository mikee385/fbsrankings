"""Storage classes for the sqlite3 repositories of the fbsrankings package"""

from fbsrankings.infrastructure.sqlite.storage.affiliation import SubdivisionTable, AffiliationTable
from fbsrankings.infrastructure.sqlite.storage.game import GameStatusTable, GameTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonSectionTable, SeasonTable
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable
from fbsrankings.infrastructure.sqlite.storage.storage import Storage

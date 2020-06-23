"""Storage classes for the sqlite3 repositories of the fbsrankings package"""

from fbsrankings.infrastructure.sqlite.storage.affiliation import (
    AffiliationTable as AffiliationTable,
)
from fbsrankings.infrastructure.sqlite.storage.affiliation import (
    SubdivisionTable as SubdivisionTable,
)
from fbsrankings.infrastructure.sqlite.storage.game import (
    GameStatusTable as GameStatusTable,
)
from fbsrankings.infrastructure.sqlite.storage.game import GameTable as GameTable
from fbsrankings.infrastructure.sqlite.storage.season import (
    SeasonSectionTable as SeasonSectionTable,
)
from fbsrankings.infrastructure.sqlite.storage.season import SeasonTable as SeasonTable
from fbsrankings.infrastructure.sqlite.storage.storage import Storage as Storage
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable as TeamTable

"""Write-model for the sqlite3 repositories of the fbsrankings package"""
from fbsrankings.infrastructure.sqlite.write.affiliation import (
    AffiliationRepository as AffiliationRepository,
)
from fbsrankings.infrastructure.sqlite.write.game import (
    GameRepository as GameRepository,
)
from fbsrankings.infrastructure.sqlite.write.ranking import (
    GameRankingRepository as GameRankingRepository,
)
from fbsrankings.infrastructure.sqlite.write.ranking import (
    TeamRankingRepository as TeamRankingRepository,
)
from fbsrankings.infrastructure.sqlite.write.record import (
    TeamRecordRepository as TeamRecordRepository,
)
from fbsrankings.infrastructure.sqlite.write.season import (
    SeasonRepository as SeasonRepository,
)
from fbsrankings.infrastructure.sqlite.write.team import (
    TeamRepository as TeamRepository,
)
from fbsrankings.infrastructure.sqlite.write.transaction import (
    Transaction as Transaction,
)

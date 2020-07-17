"""Write-model for the in-memory repositories of the fbsrankings package"""
from fbsrankings.infrastructure.memory.write.affiliation import (
    AffiliationRepository as AffiliationRepository,
)
from fbsrankings.infrastructure.memory.write.game import (
    GameRepository as GameRepository,
)
from fbsrankings.infrastructure.memory.write.ranking import (
    GameRankingRepository as GameRankingRepository,
)
from fbsrankings.infrastructure.memory.write.ranking import (
    TeamRankingRepository as TeamRankingRepository,
)
from fbsrankings.infrastructure.memory.write.record import (
    TeamRecordRepository as TeamRecordRepository,
)
from fbsrankings.infrastructure.memory.write.season import (
    SeasonRepository as SeasonRepository,
)
from fbsrankings.infrastructure.memory.write.team import (
    TeamRepository as TeamRepository,
)
from fbsrankings.infrastructure.memory.write.transaction import (
    Transaction as Transaction,
)

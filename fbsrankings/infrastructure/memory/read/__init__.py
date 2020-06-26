"""Read-model for the in-memory repositories of the fbsrankings package"""
from fbsrankings.infrastructure.memory.read.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler as AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.read.canceled_games import (
    CanceledGamesQueryHandler as CanceledGamesQueryHandler,
)
from fbsrankings.infrastructure.memory.read.game_by_id import (
    GameByIDQueryHandler as GameByIDQueryHandler,
)
from fbsrankings.infrastructure.memory.read.game_count_by_season import (
    GameCountBySeasonQueryHandler as GameCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.memory.read.query_manager import (
    QueryManager as QueryManager,
)
from fbsrankings.infrastructure.memory.read.season_by_id import (
    SeasonByIDQueryHandler as SeasonByIDQueryHandler,
)
from fbsrankings.infrastructure.memory.read.seasons import (
    SeasonsQueryHandler as SeasonsQueryHandler,
)
from fbsrankings.infrastructure.memory.read.team_by_id import (
    TeamByIDQueryHandler as TeamByIDQueryHandler,
)
from fbsrankings.infrastructure.memory.read.team_count_by_season import (
    TeamCountBySeasonQueryHandler as TeamCountBySeasonQueryHandler,
)

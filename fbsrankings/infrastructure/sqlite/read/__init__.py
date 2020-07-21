"""Read-model for the sqlite3 repositories of the fbsrankings package"""
from fbsrankings.infrastructure.sqlite.read.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler as AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.canceled_games import (
    CanceledGamesQueryHandler as CanceledGamesQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.game_by_id import (
    GameByIDQueryHandler as GameByIDQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.game_count_by_season import (
    GameCountBySeasonQueryHandler as GameCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.most_recent_completed_week import (
    MostRecentCompletedWeekQueryHandler as MostRecentCompletedWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.query_manager import (
    QueryManager as QueryManager,
)
from fbsrankings.infrastructure.sqlite.read.season_by_id import (
    SeasonByIDQueryHandler as SeasonByIDQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.seasons import (
    SeasonsQueryHandler as SeasonsQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_by_id import (
    TeamByIDQueryHandler as TeamByIDQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_count_by_season import (
    TeamCountBySeasonQueryHandler as TeamCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler as TeamRankingBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler as TeamRecordBySeasonWeekQueryHandler,
)

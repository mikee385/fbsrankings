import sqlite3

from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManager as BaseQueryManager
from fbsrankings.infrastructure.sqlite.read.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.canceled_games import (
    CanceledGamesQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.game_by_id import GameByIDQueryHandler
from fbsrankings.infrastructure.sqlite.read.game_count_by_season import (
    GameCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.most_recent_completed_week import (
    MostRecentCompletedWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.season_by_id import SeasonByIDQueryHandler
from fbsrankings.infrastructure.sqlite.read.season_by_year import (
    SeasonByYearQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.seasons import SeasonsQueryHandler
from fbsrankings.infrastructure.sqlite.read.team_by_id import TeamByIDQueryHandler
from fbsrankings.infrastructure.sqlite.read.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler,
)
from fbsrankings.infrastructure.sqlite.read.week_count_by_season import (
    WeekCountBySeasonQueryHandler,
)
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import MostRecentCompletedWeekQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import WeekCountBySeasonQuery


class QueryManager(BaseQueryManager):
    def __init__(self, connection: sqlite3.Connection, query_bus: QueryBus) -> None:
        super().__init__(query_bus)

        self._connection = connection

        self.register_handler(
            AffiliationCountBySeasonQuery,
            AffiliationCountBySeasonQueryHandler(self._connection),
        )
        self.register_handler(
            CanceledGamesQuery, CanceledGamesQueryHandler(self._connection)
        )
        self.register_handler(GameByIDQuery, GameByIDQueryHandler(self._connection))
        self.register_handler(
            GameCountBySeasonQuery, GameCountBySeasonQueryHandler(self._connection)
        )
        self.register_handler(
            GameRankingBySeasonWeekQuery,
            GameRankingBySeasonWeekQueryHandler(self._connection),
        )
        self.register_handler(
            MostRecentCompletedWeekQuery,
            MostRecentCompletedWeekQueryHandler(self._connection),
        )
        self.register_handler(SeasonByIDQuery, SeasonByIDQueryHandler(self._connection))
        self.register_handler(
            SeasonByYearQuery, SeasonByYearQueryHandler(self._connection)
        )
        self.register_handler(SeasonsQuery, SeasonsQueryHandler(self._connection))
        self.register_handler(TeamByIDQuery, TeamByIDQueryHandler(self._connection))
        self.register_handler(
            TeamCountBySeasonQuery, TeamCountBySeasonQueryHandler(self._connection)
        )
        self.register_handler(
            TeamRankingBySeasonWeekQuery,
            TeamRankingBySeasonWeekQueryHandler(self._connection),
        )
        self.register_handler(
            TeamRecordBySeasonWeekQuery,
            TeamRecordBySeasonWeekQueryHandler(self._connection),
        )
        self.register_handler(
            WeekCountBySeasonQuery, WeekCountBySeasonQueryHandler(self._connection)
        )

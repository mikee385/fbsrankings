from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional

from communication.bus import QueryBus
from fbsrankings.core.query.infrastructure.sqlite.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.affiliations_by_season import (
    AffiliationsBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.canceled_games import (
    CanceledGamesQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.game_by_id import GameByIDQueryHandler
from fbsrankings.core.query.infrastructure.sqlite.game_count_by_season import (
    GameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.games_by_season import (
    GamesBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.latest_season_week import (
    LatestSeasonWeekQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.season_by_id import (
    SeasonByIDQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.season_by_year import (
    SeasonByYearQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.seasons import SeasonsQueryHandler
from fbsrankings.core.query.infrastructure.sqlite.team_by_id import TeamByIDQueryHandler
from fbsrankings.core.query.infrastructure.sqlite.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.sqlite.teams import TeamsQueryHandler
from fbsrankings.core.query.infrastructure.sqlite.week_count_by_season import (
    WeekCountBySeasonQueryHandler,
)
from fbsrankings.messages.query import AffiliationCountBySeasonQuery
from fbsrankings.messages.query import AffiliationsBySeasonQuery
from fbsrankings.messages.query import CanceledGamesQuery
from fbsrankings.messages.query import GameByIDQuery
from fbsrankings.messages.query import GameCountBySeasonQuery
from fbsrankings.messages.query import GamesBySeasonQuery
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import PostseasonGameCountBySeasonQuery
from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamsQuery
from fbsrankings.messages.query import WeekCountBySeasonQuery
from fbsrankings.storage.sqlite import Storage


class QueryManager(ContextManager["QueryManager"]):
    def __init__(self, storage: Storage, bus: QueryBus) -> None:
        self._bus = bus

        self._bus.register_handler(
            AffiliationCountBySeasonQuery,
            AffiliationCountBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            AffiliationsBySeasonQuery,
            AffiliationsBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            CanceledGamesQuery,
            CanceledGamesQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            GameByIDQuery,
            GameByIDQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            GameCountBySeasonQuery,
            GameCountBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            GamesBySeasonQuery,
            GamesBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            LatestSeasonWeekQuery,
            LatestSeasonWeekQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            PostseasonGameCountBySeasonQuery,
            PostseasonGameCountBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            SeasonByIDQuery,
            SeasonByIDQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            SeasonByYearQuery,
            SeasonByYearQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            SeasonsQuery,
            SeasonsQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            TeamByIDQuery,
            TeamByIDQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            TeamCountBySeasonQuery,
            TeamCountBySeasonQueryHandler(storage.connection),
        )
        self._bus.register_handler(TeamsQuery, TeamsQueryHandler(storage.connection))
        self._bus.register_handler(
            WeekCountBySeasonQuery,
            WeekCountBySeasonQueryHandler(storage.connection),
        )

    def close(self) -> None:
        self._bus.unregister_handler(AffiliationCountBySeasonQuery)
        self._bus.unregister_handler(AffiliationsBySeasonQuery)
        self._bus.unregister_handler(CanceledGamesQuery)
        self._bus.unregister_handler(GameByIDQuery)
        self._bus.unregister_handler(GameCountBySeasonQuery)
        self._bus.unregister_handler(GamesBySeasonQuery)
        self._bus.unregister_handler(LatestSeasonWeekQuery)
        self._bus.unregister_handler(PostseasonGameCountBySeasonQuery)
        self._bus.unregister_handler(SeasonByIDQuery)
        self._bus.unregister_handler(SeasonByYearQuery)
        self._bus.unregister_handler(SeasonsQuery)
        self._bus.unregister_handler(TeamByIDQuery)
        self._bus.unregister_handler(TeamCountBySeasonQuery)
        self._bus.unregister_handler(TeamsQuery)
        self._bus.unregister_handler(WeekCountBySeasonQuery)

    def __enter__(self) -> "QueryManager":
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.core.query.infrastructure.memory.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.affiliations_by_season import (
    AffiliationsBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.canceled_games import (
    CanceledGamesQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.game_by_id import GameByIDQueryHandler
from fbsrankings.core.query.infrastructure.memory.game_count_by_season import (
    GameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.games_by_season import (
    GamesBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.latest_season_week import (
    LatestSeasonWeekQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.season_by_id import (
    SeasonByIDQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.season_by_year import (
    SeasonByYearQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.seasons import SeasonsQueryHandler
from fbsrankings.core.query.infrastructure.memory.team_by_id import TeamByIDQueryHandler
from fbsrankings.core.query.infrastructure.memory.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.memory.teams import TeamsQueryHandler
from fbsrankings.core.query.infrastructure.memory.week_count_by_season import (
    WeekCountBySeasonQueryHandler,
)
from fbsrankings.shared.messaging import QueryBus
from fbsrankings.shared.query import AffiliationCountBySeasonQuery
from fbsrankings.shared.query import AffiliationsBySeasonQuery
from fbsrankings.shared.query import CanceledGamesQuery
from fbsrankings.shared.query import GameByIDQuery
from fbsrankings.shared.query import GameCountBySeasonQuery
from fbsrankings.shared.query import GamesBySeasonQuery
from fbsrankings.shared.query import LatestSeasonWeekQuery
from fbsrankings.shared.query import PostseasonGameCountBySeasonQuery
from fbsrankings.shared.query import SeasonByIDQuery
from fbsrankings.shared.query import SeasonByYearQuery
from fbsrankings.shared.query import SeasonsQuery
from fbsrankings.shared.query import TeamByIDQuery
from fbsrankings.shared.query import TeamCountBySeasonQuery
from fbsrankings.shared.query import TeamsQuery
from fbsrankings.shared.query import WeekCountBySeasonQuery
from fbsrankings.storage.memory import Storage


class QueryManager(ContextManager["QueryManager"]):
    def __init__(self, storage: Storage, bus: QueryBus) -> None:
        self._bus = bus

        self._bus.register_handler(
            AffiliationCountBySeasonQuery,
            AffiliationCountBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(
            AffiliationsBySeasonQuery,
            AffiliationsBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(
            CanceledGamesQuery,
            CanceledGamesQueryHandler(storage),
        )
        self._bus.register_handler(GameByIDQuery, GameByIDQueryHandler(storage))
        self._bus.register_handler(
            GameCountBySeasonQuery,
            GameCountBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(
            GamesBySeasonQuery,
            GamesBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(
            LatestSeasonWeekQuery,
            LatestSeasonWeekQueryHandler(storage),
        )
        self._bus.register_handler(
            PostseasonGameCountBySeasonQuery,
            PostseasonGameCountBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(SeasonByIDQuery, SeasonByIDQueryHandler(storage))
        self._bus.register_handler(SeasonByYearQuery, SeasonByYearQueryHandler(storage))
        self._bus.register_handler(SeasonsQuery, SeasonsQueryHandler(storage))
        self._bus.register_handler(TeamByIDQuery, TeamByIDQueryHandler(storage))
        self._bus.register_handler(
            TeamCountBySeasonQuery,
            TeamCountBySeasonQueryHandler(storage),
        )
        self._bus.register_handler(TeamsQuery, TeamsQueryHandler(storage))
        self._bus.register_handler(
            WeekCountBySeasonQuery,
            WeekCountBySeasonQueryHandler(storage),
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
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False

from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.core.query.infrastructure.tinydb.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.affiliation_count_by_season import (
    AffiliationCountBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.affiliations_by_season import (
    AffiliationsBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.affiliations_by_season import (
    AffiliationsBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.canceled_games import (
    CanceledGamesQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.canceled_games import (
    CanceledGamesQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.game_by_id import GameByIDQueryHandler
from fbsrankings.core.query.infrastructure.tinydb.game_count_by_season import (
    GameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.game_count_by_season import (
    GameCountBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.games_by_season import (
    GamesBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.games_by_season import (
    GamesBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.latest_season_week import (
    LatestSeasonWeekQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.latest_season_week import (
    LatestSeasonWeekQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.season_by_id import (
    SeasonByIDQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.season_by_year import (
    SeasonByYearQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.seasons import SeasonsQueryHandler
from fbsrankings.core.query.infrastructure.tinydb.seasons import SeasonsQueryProjection
from fbsrankings.core.query.infrastructure.tinydb.team_by_id import TeamByIDQueryHandler
from fbsrankings.core.query.infrastructure.tinydb.team_count_by_season import (
    TeamCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.team_count_by_season import (
    TeamCountBySeasonQueryProjection,
)
from fbsrankings.core.query.infrastructure.tinydb.teams import TeamsQueryHandler
from fbsrankings.core.query.infrastructure.tinydb.teams import TeamsQueryProjection
from fbsrankings.core.query.infrastructure.tinydb.week_count_by_season import (
    WeekCountBySeasonQueryHandler,
)
from fbsrankings.core.query.infrastructure.tinydb.week_count_by_season import (
    WeekCountBySeasonQueryProjection,
)
from fbsrankings.shared.messaging import EventBus
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
from fbsrankings.storage.tinydb import Storage


class QueryManager(ContextManager["QueryManager"]):
    def __init__(
        self,
        storage: Storage,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        self._query_bus = query_bus

        self._affiliation_count_by_season_projection = (
            AffiliationCountBySeasonQueryProjection(
                storage,
                event_bus,
            )
        )
        self._affiliations_projection = AffiliationsBySeasonQueryProjection(
            storage,
            event_bus,
        )
        self._canceled_games_projection = CanceledGamesQueryProjection(
            storage,
            event_bus,
        )
        self._game_count_by_season_projection = GameCountBySeasonQueryProjection(
            storage,
            event_bus,
        )
        self._games_projection = GamesBySeasonQueryProjection(storage, event_bus)
        self._latest_season_week_projection = LatestSeasonWeekQueryProjection(
            storage,
            event_bus,
        )
        self._postseason_game_count_by_season_projection = (
            PostseasonGameCountBySeasonQueryProjection(
                storage,
                event_bus,
            )
        )
        self._seasons_projection = SeasonsQueryProjection(storage, event_bus)
        self._team_count_by_season_projection = TeamCountBySeasonQueryProjection(
            storage,
            event_bus,
        )
        self._teams_projection = TeamsQueryProjection(storage, event_bus)
        self._week_count_by_season_projection = WeekCountBySeasonQueryProjection(
            storage,
            event_bus,
        )

        self._query_bus.register_handler(
            AffiliationCountBySeasonQuery,
            AffiliationCountBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(
            AffiliationsBySeasonQuery,
            AffiliationsBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(
            CanceledGamesQuery,
            CanceledGamesQueryHandler(storage),
        )
        self._query_bus.register_handler(
            GameByIDQuery,
            GameByIDQueryHandler(storage),
        )
        self._query_bus.register_handler(
            GameCountBySeasonQuery,
            GameCountBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(
            GamesBySeasonQuery,
            GamesBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(
            LatestSeasonWeekQuery,
            LatestSeasonWeekQueryHandler(storage),
        )
        self._query_bus.register_handler(
            PostseasonGameCountBySeasonQuery,
            PostseasonGameCountBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(
            SeasonByIDQuery,
            SeasonByIDQueryHandler(storage),
        )
        self._query_bus.register_handler(
            SeasonByYearQuery,
            SeasonByYearQueryHandler(storage),
        )
        self._query_bus.register_handler(SeasonsQuery, SeasonsQueryHandler(storage))
        self._query_bus.register_handler(
            TeamByIDQuery,
            TeamByIDQueryHandler(storage),
        )
        self._query_bus.register_handler(
            TeamCountBySeasonQuery,
            TeamCountBySeasonQueryHandler(storage),
        )
        self._query_bus.register_handler(TeamsQuery, TeamsQueryHandler(storage))
        self._query_bus.register_handler(
            WeekCountBySeasonQuery,
            WeekCountBySeasonQueryHandler(storage),
        )

    def close(self) -> None:
        self._query_bus.unregister_handler(AffiliationCountBySeasonQuery)
        self._query_bus.unregister_handler(AffiliationsBySeasonQuery)
        self._query_bus.unregister_handler(CanceledGamesQuery)
        self._query_bus.unregister_handler(GameByIDQuery)
        self._query_bus.unregister_handler(GameCountBySeasonQuery)
        self._query_bus.unregister_handler(GamesBySeasonQuery)
        self._query_bus.unregister_handler(LatestSeasonWeekQuery)
        self._query_bus.unregister_handler(PostseasonGameCountBySeasonQuery)
        self._query_bus.unregister_handler(SeasonByIDQuery)
        self._query_bus.unregister_handler(SeasonByYearQuery)
        self._query_bus.unregister_handler(SeasonsQuery)
        self._query_bus.unregister_handler(TeamByIDQuery)
        self._query_bus.unregister_handler(TeamCountBySeasonQuery)
        self._query_bus.unregister_handler(TeamsQuery)
        self._query_bus.unregister_handler(WeekCountBySeasonQuery)

        self._affiliation_count_by_season_projection.close()
        self._affiliations_projection.close()
        self._canceled_games_projection.close()
        self._game_count_by_season_projection.close()
        self._games_projection.close()
        self._latest_season_week_projection.close()
        self._postseason_game_count_by_season_projection.close()
        self._seasons_projection.close()
        self._team_count_by_season_projection.close()
        self._teams_projection.close()
        self._week_count_by_season_projection.close()

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

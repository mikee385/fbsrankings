from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from communication.bus import EventBus
from communication.bus import QueryBus
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.ranking.query.infrastructure.tinydb.game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryHandler,
)
from fbsrankings.ranking.query.infrastructure.tinydb.game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryProjection,
)
from fbsrankings.ranking.query.infrastructure.tinydb.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler,
)
from fbsrankings.ranking.query.infrastructure.tinydb.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryProjection,
)
from fbsrankings.ranking.query.infrastructure.tinydb.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler,
)
from fbsrankings.ranking.query.infrastructure.tinydb.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryProjection,
)
from fbsrankings.storage.tinydb import Storage


class QueryManager(ContextManager["QueryManager"]):
    def __init__(
        self,
        storage: Storage,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        self._query_bus = query_bus

        self._game_ranking_by_season_week_projection = (
            GameRankingBySeasonWeekQueryProjection(
                storage,
                event_bus,
            )
        )
        self._team_ranking_by_season_week_projection = (
            TeamRankingBySeasonWeekQueryProjection(
                storage,
                event_bus,
            )
        )
        self._team_record_by_season_week_projection = (
            TeamRecordBySeasonWeekQueryProjection(
                storage,
                event_bus,
            )
        )

        self._query_bus.register_handler(
            GameRankingBySeasonWeekQuery,
            GameRankingBySeasonWeekQueryHandler(storage),
        )
        self._query_bus.register_handler(
            TeamRankingBySeasonWeekQuery,
            TeamRankingBySeasonWeekQueryHandler(storage),
        )
        self._query_bus.register_handler(
            TeamRecordBySeasonWeekQuery,
            TeamRecordBySeasonWeekQueryHandler(storage),
        )

    def close(self) -> None:
        self._query_bus.unregister_handler(GameRankingBySeasonWeekQuery)
        self._query_bus.unregister_handler(TeamRankingBySeasonWeekQuery)
        self._query_bus.unregister_handler(TeamRecordBySeasonWeekQuery)

        self._game_ranking_by_season_week_projection.close()
        self._team_ranking_by_season_week_projection.close()
        self._team_record_by_season_week_projection.close()

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

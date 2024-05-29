from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.ranking.query.infrastructure.sqlite.game_ranking_by_season_week import (
    GameRankingBySeasonWeekQueryHandler,
)
from fbsrankings.ranking.query.infrastructure.sqlite.team_ranking_by_season_week import (
    TeamRankingBySeasonWeekQueryHandler,
)
from fbsrankings.ranking.query.infrastructure.sqlite.team_record_by_season_week import (
    TeamRecordBySeasonWeekQueryHandler,
)
from fbsrankings.shared.messaging import QueryBus
from fbsrankings.shared.query import GameRankingBySeasonWeekQuery
from fbsrankings.shared.query import TeamRankingBySeasonWeekQuery
from fbsrankings.shared.query import TeamRecordBySeasonWeekQuery
from fbsrankings.storage.sqlite import Storage


class QueryManager(ContextManager["QueryManager"]):
    def __init__(self, storage: Storage, bus: QueryBus) -> None:
        self._bus = bus

        self._bus.register_handler(
            GameRankingBySeasonWeekQuery,
            GameRankingBySeasonWeekQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            TeamRankingBySeasonWeekQuery,
            TeamRankingBySeasonWeekQueryHandler(storage.connection),
        )
        self._bus.register_handler(
            TeamRecordBySeasonWeekQuery,
            TeamRecordBySeasonWeekQueryHandler(storage.connection),
        )

    def close(self) -> None:
        self._bus.unregister_handler(GameRankingBySeasonWeekQuery)
        self._bus.unregister_handler(TeamRankingBySeasonWeekQuery)
        self._bus.unregister_handler(TeamRecordBySeasonWeekQuery)

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

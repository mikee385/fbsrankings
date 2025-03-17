from types import TracebackType
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from fbsrankings.ranking.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    GameRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    TeamRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.memory.record import (
    TeamRecordEventHandler,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    GameRankingEventManager,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    TeamRankingEventManager,
)
from fbsrankings.ranking.command.infrastructure.shared.record import (
    TeamRecordEventManager,
)
from fbsrankings.storage.memory import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._team_record = TeamRecordEventManager(
            TeamRecordEventHandler(storage.team_record),
            bus,
        )
        self._team_ranking = TeamRankingEventManager(
            TeamRankingEventHandler(storage.team_ranking),
            bus,
        )
        self._game_ranking = GameRankingEventManager(
            GameRankingEventHandler(storage.game_ranking),
            bus,
        )

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

    def __enter__(self) -> "EventHandler":
        self._team_record.__enter__()
        self._team_ranking.__enter__()
        self._game_ranking.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        self._game_ranking.__exit__(type_, value, traceback)
        self._team_ranking.__exit__(type_, value, traceback)
        self._team_record.__exit__(type_, value, traceback)
        return False

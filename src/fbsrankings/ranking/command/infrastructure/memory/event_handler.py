from fbsrankings.common import EventBus
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
from fbsrankings.storage.memory import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._team_record = TeamRecordEventHandler(storage.team_record, bus)
        self._team_ranking = TeamRankingEventHandler(storage.team_ranking, bus)
        self._game_ranking = GameRankingEventHandler(storage.game_ranking, bus)

    def close(self) -> None:
        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

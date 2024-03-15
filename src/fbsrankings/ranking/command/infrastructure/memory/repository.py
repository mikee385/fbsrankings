from fbsrankings.common import EventBus
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    GameRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    TeamRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.record import (
    TeamRecordRepository,
)
from fbsrankings.ranking.command.infrastructure.repository import (
    Repository as BaseRepository,
)
from fbsrankings.storage.memory import Storage


class Repository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = bus

        self._team_record = TeamRecordRepository(storage.team_record, self._bus)
        self._team_ranking = TeamRankingRepository(storage.team_ranking, self._bus)
        self._game_ranking = GameRankingRepository(storage.game_ranking, self._bus)

    @property
    def team_record(self) -> TeamRecordRepository:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

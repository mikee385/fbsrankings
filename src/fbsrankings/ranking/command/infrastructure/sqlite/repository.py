from communication.bus import EventBus
from fbsrankings.ranking.command.domain.model.repository import (
    Repository as BaseRepository,
)
from fbsrankings.ranking.command.infrastructure.sqlite.ranking import (
    GameRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.sqlite.ranking import (
    TeamRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.sqlite.record import (
    TeamRecordRepository,
)
from fbsrankings.storage.sqlite import Storage


class Repository(BaseRepository):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._team_record = TeamRecordRepository(storage.connection, bus)
        self._team_ranking = TeamRankingRepository(storage.connection, bus)
        self._game_ranking = GameRankingRepository(storage.connection, bus)

    @property
    def team_record(self) -> TeamRecordRepository:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

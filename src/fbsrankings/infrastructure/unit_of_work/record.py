from typing import List
from typing import Optional

from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamRecord
from fbsrankings.domain import TeamRecordID
from fbsrankings.domain import TeamRecordRepository as BaseRepository
from fbsrankings.domain import TeamRecordValue
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.memory.storage import (
    TeamRecordStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    TeamRecordRepository as MemoryRepository,
)


class TeamRecordRepository(BaseRepository):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(
            TeamRecordCalculatedEvent,
            self._cache.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRecordCalculatedEvent,
            self._cache.handle_calculated,
        )

    def create(
        self,
        season_id: SeasonID,
        week: Optional[int],
        values: List[TeamRecordValue],
    ) -> TeamRecord:
        return self._repository.create(season_id, week, values)

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        team_record = self._cache.get(id_)
        if team_record is None:
            team_record = self._repository.get(id_)
        return team_record

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        team_record = self._cache.find(season_id, week)
        if team_record is None:
            team_record = self._repository.find(season_id, week)
        return team_record

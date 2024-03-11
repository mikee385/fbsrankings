from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamRecord
from fbsrankings.domain import TeamRecordEventHandler as BaseEventHandler
from fbsrankings.domain import TeamRecordID
from fbsrankings.domain import TeamRecordRepository as BaseRepository
from fbsrankings.domain import TeamRecordValue
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.memory.write import (
    TeamRecordRepository as MemoryRepository,
)


class TeamRecordRepository(BaseRepository):
    def __init__(self, repository: BaseRepository, cache: MemoryRepository) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

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


class TeamRecordEventHandler(BaseEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._events.append(event)

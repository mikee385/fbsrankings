from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRecord
from fbsrankings.domain import TeamRecordID
from fbsrankings.domain import TeamRecordRepository as BaseRepository
from fbsrankings.domain import TeamRecordValue
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.memory.storage import TeamRecordDto
from fbsrankings.infrastructure.memory.storage import TeamRecordStorage
from fbsrankings.infrastructure.memory.storage import TeamRecordValueDto


class TeamRecordRepository(BaseRepository):
    def __init__(self, storage: TeamRecordStorage, bus: EventBus) -> None:
        self._bus = bus
        self._storage = storage

    def get(self, ID: TeamRecordID) -> Optional[TeamRecord]:
        dto = self._storage.get(ID.value)
        return self._to_record(dto) if dto is not None else None

    def find(self, season_ID: SeasonID, week: Optional[int],) -> Optional[TeamRecord]:
        dto = self._storage.find(season_ID.value, week)
        return self._to_record(dto) if dto is not None else None

    def _to_record(self, dto: TeamRecordDto) -> TeamRecord:
        return TeamRecord(
            self._bus,
            TeamRecordID(dto.ID),
            SeasonID(dto.season_ID),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )

    def _to_value(self, dto: TeamRecordValueDto) -> TeamRecordValue:
        return TeamRecordValue(TeamID(dto.team_ID), dto.wins, dto.losses)

    def handle(self, event: Event) -> bool:
        if isinstance(event, TeamRecordCalculatedEvent):
            self._handle_record_calculated(event)
            return True
        else:
            return False

    def _handle_record_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._storage.add(
            TeamRecordDto(
                event.ID,
                event.season_ID,
                event.week,
                [
                    TeamRecordValueDto(value.team_ID, value.wins, value.losses)
                    for value in event.values
                ],
            )
        )